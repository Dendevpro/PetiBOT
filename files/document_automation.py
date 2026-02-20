"""
Document Automation Script for Legal Documents
Processes Word documents: extracts text, generates summary with Gemini,
creates QR code, converts to PDF, and adds QR code to header.
"""

import os
import io
import json
import base64
import requests
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

# Third-party imports (will need to be installed)
try:
    from docx import Document
    from PIL import Image
    from PyPDF2 import PdfReader, PdfWriter
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    import google.generativeai as genai
except ImportError as e:
    print(f"Missing required library: {e}")
    print("Please run: pip install python-docx Pillow PyPDF2 reportlab google-generativeai")


class DocumentAutomation:
    """Main class for document automation workflow"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the automation with configuration
        
        Args:
            config: Dictionary containing API keys and settings
        """
        self.config = config
        self.gemini_api_key = config.get('gemini_api_key')
        self.email_config = config.get('email', {})
        self.output_dir = Path(config.get('output_dir', 'output'))
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize Gemini
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-pro')
    
    def extract_text_from_docx(self, docx_path: str) -> str:
        """
        Extract text content from a Word document
        
        Args:
            docx_path: Path to the .docx file
            
        Returns:
            Extracted text as string
        """
        try:
            doc = Document(docx_path)
            full_text = []
            
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    full_text.append(paragraph.text)
            
            return '\n'.join(full_text)
        except Exception as e:
            raise Exception(f"Error extracting text from Word document: {e}")
    
    def summarize_with_gemini(self, text: str) -> str:
        """
        Generate summary using Gemini API
        
        Args:
            text: Text to summarize
            
        Returns:
            Summary text
        """
        try:
            prompt = f"""Por favor, resuma o seguinte documento jurídico em português brasileiro. 
            O resumo deve ser conciso (máximo 500 caracteres) e destacar os pontos principais:

            {text}
            
            Resumo:"""
            
            response = self.model.generate_content(prompt)
            summary = response.text.strip()
            
            # Ensure summary fits in QR code (max ~500 chars for reasonable QR code size)
            if len(summary) > 500:
                summary = summary[:497] + "..."
            
            return summary
        except Exception as e:
            raise Exception(f"Error generating summary with Gemini: {e}")
    
    def generate_qr_code(self, text: str, output_path: str) -> str:
        """
        Generate QR code using QR Server API
        
        Args:
            text: Text to encode in QR code
            output_path: Path to save the QR code image
            
        Returns:
            Path to generated QR code
        """
        try:
            # QR Server API (free, no key needed)
            url = "https://api.qrserver.com/v1/create-qr-code/"
            
            params = {
                'data': text,
                'size': '300x300',
                'format': 'png',
                'ecc': 'L'  # Error correction level
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            # Save QR code image
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            return output_path
        except Exception as e:
            raise Exception(f"Error generating QR code: {e}")
    
    def convert_docx_to_pdf_cloudconvert(self, docx_path: str, pdf_path: str) -> str:
        """
        Convert Word document to PDF using CloudConvert API (cloud-compatible)
        
        Args:
            docx_path: Path to input .docx file
            pdf_path: Path for output .pdf file
            
        Returns:
            Path to generated PDF
        """
        try:
            api_key = self.config.get('cloudconvert_api_key')
            if not api_key:
                raise Exception(
                    "CloudConvert API key not configured. "
                    "Get free key at: https://cloudconvert.com/register"
                )
            
            import time
            
            # CloudConvert API endpoint
            base_url = "https://api.cloudconvert.com/v2"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            # Step 1: Create a job
            job_data = {
                "tasks": {
                    "import-my-file": {
                        "operation": "import/upload"
                    },
                    "convert-my-file": {
                        "operation": "convert",
                        "input": "import-my-file",
                        "output_format": "pdf"
                    },
                    "export-my-file": {
                        "operation": "export/url",
                        "input": "convert-my-file"
                    }
                }
            }
            
            response = requests.post(f"{base_url}/jobs", headers=headers, json=job_data)
            response.raise_for_status()
            job = response.json()
            
            # Step 2: Upload file
            upload_task = next(t for t in job['data']['tasks'] if t['name'] == 'import-my-file')
            upload_url = upload_task['result']['form']['url']
            upload_params = upload_task['result']['form']['parameters']
            
            with open(docx_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(upload_url, data=upload_params, files=files)
                response.raise_for_status()
            
            # Step 3: Wait for conversion
            job_id = job['data']['id']
            max_wait = 60  # seconds
            start_time = time.time()
            
            while time.time() - start_time < max_wait:
                response = requests.get(f"{base_url}/jobs/{job_id}", headers=headers)
                response.raise_for_status()
                job_status = response.json()
                
                if job_status['data']['status'] == 'finished':
                    break
                elif job_status['data']['status'] == 'error':
                    raise Exception("CloudConvert conversion failed")
                
                time.sleep(2)
            
            # Step 4: Download converted file
            export_task = next(t for t in job_status['data']['tasks'] if t['name'] == 'export-my-file')
            download_url = export_task['result']['files'][0]['url']
            
            response = requests.get(download_url)
            response.raise_for_status()
            
            with open(pdf_path, 'wb') as f:
                f.write(response.content)
            
            return pdf_path
            
        except Exception as e:
            raise Exception(f"Error converting to PDF with CloudConvert: {e}")
    
    def convert_docx_to_pdf_libreoffice(self, docx_path: str, pdf_path: str) -> str:
        """
        Convert Word document to PDF using LibreOffice (local only)
        
        Args:
            docx_path: Path to input .docx file
            pdf_path: Path for output .pdf file
            
        Returns:
            Path to generated PDF
        """
        try:
            import subprocess
            
            # Try using LibreOffice command line (works on Windows, Mac, Linux)
            output_dir = str(Path(pdf_path).parent)
            
            # LibreOffice command
            cmd = [
                'soffice',  # or 'libreoffice' on some systems
                '--headless',
                '--convert-to', 'pdf',
                '--outdir', output_dir,
                docx_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                raise Exception(f"LibreOffice conversion failed: {result.stderr}")
            
            # LibreOffice creates file with same name as input
            generated_pdf = Path(output_dir) / (Path(docx_path).stem + '.pdf')
            
            if generated_pdf.exists() and str(generated_pdf) != pdf_path:
                generated_pdf.rename(pdf_path)
            
            return pdf_path
        except FileNotFoundError:
            raise Exception(
                "LibreOffice not found. Please install LibreOffice: "
                "https://www.libreoffice.org/download/"
            )
        except Exception as e:
            raise Exception(f"Error converting to PDF: {e}")
    
    def convert_docx_to_pdf(self, docx_path: str, pdf_path: str) -> str:
        """
        Convert Word document to PDF (auto-detects best method)
        
        Args:
            docx_path: Path to input .docx file
            pdf_path: Path for output .pdf file
            
        Returns:
            Path to generated PDF
        """
        # Check if CloudConvert API key is available (cloud deployment)
        if self.config.get('cloudconvert_api_key'):
            return self.convert_docx_to_pdf_cloudconvert(docx_path, pdf_path)
        else:
            # Try LibreOffice (local deployment)
            return self.convert_docx_to_pdf_libreoffice(docx_path, pdf_path)
    
    def add_qr_to_pdf_header(self, pdf_path: str, qr_image_path: str, output_path: str) -> str:
        """
        Add QR code to PDF header with "Resumo" text
        
        Args:
            pdf_path: Path to input PDF
            qr_image_path: Path to QR code image
            output_path: Path for output PDF with QR code
            
        Returns:
            Path to final PDF
        """
        try:
            # Read existing PDF
            reader = PdfReader(pdf_path)
            writer = PdfWriter()
            
            # Create overlay with QR code
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)
            
            # Position QR code in top-right corner with "Resumo" label
            page_width, page_height = letter
            qr_size = 80  # Size of QR code in points
            margin = 50
            
            # Add "Resumo" text above QR code
            can.setFont("Helvetica-Bold", 10)
            can.drawString(page_width - margin - qr_size, page_height - margin + 15, "Resumo")
            
            # Add QR code image
            can.drawImage(
                qr_image_path,
                page_width - margin - qr_size,
                page_height - margin - qr_size,
                width=qr_size,
                height=qr_size,
                preserveAspectRatio=True
            )
            
            can.save()
            packet.seek(0)
            
            # Read the overlay PDF
            overlay_pdf = PdfReader(packet)
            
            # Add QR code to all pages
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                page.merge_page(overlay_pdf.pages[0])
                writer.add_page(page)
            
            # Write output
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            return output_path
        except Exception as e:
            raise Exception(f"Error adding QR code to PDF: {e}")
    
    def send_email(self, pdf_path: str, recipient: str, summary: str) -> bool:
        """
        Send email with PDF attachment
        
        Args:
            pdf_path: Path to PDF file
            recipient: Email address to send to
            summary: Document summary for email body
            
        Returns:
            True if successful
        """
        try:
            sender = self.email_config.get('sender')
            password = self.email_config.get('password')
            smtp_server = self.email_config.get('smtp_server', 'smtp.gmail.com')
            smtp_port = self.email_config.get('smtp_port', 587)
            
            if not all([sender, password, recipient]):
                raise Exception("Email configuration incomplete")
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = recipient
            msg['Subject'] = f'Documento Processado - {Path(pdf_path).stem}'
            
            # Email body
            body = f"""
Olá,

Seu documento foi processado com sucesso.

Resumo:
{summary}

O documento completo com QR code está anexado.

Atenciosamente,
Sistema de Automação de Documentos
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach PDF
            with open(pdf_path, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
            
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename={Path(pdf_path).name}'
            )
            msg.attach(part)
            
            # Send email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender, password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            raise Exception(f"Error sending email: {e}")
    
    def process_document(
        self,
        docx_path: str,
        recipient_email: Optional[str] = None,
        send_email: bool = True
    ) -> Dict[str, Any]:
        """
        Complete workflow: process document from start to finish
        
        Args:
            docx_path: Path to Word document
            recipient_email: Email to send final PDF to
            send_email: Whether to send email
            
        Returns:
            Dictionary with results and paths
        """
        results = {
            'success': False,
            'timestamp': datetime.now().isoformat(),
            'input_file': docx_path,
        }
        
        try:
            filename = Path(docx_path).stem
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # Step 1: Extract text
            print("📄 Extracting text from Word document...")
            text = self.extract_text_from_docx(docx_path)
            results['text_length'] = len(text)
            
            # Step 2: Generate summary with Gemini
            print("🤖 Generating summary with Gemini...")
            summary = self.summarize_with_gemini(text)
            results['summary'] = summary
            print(f"✓ Summary generated ({len(summary)} characters)")
            
            # Step 3: Generate QR code
            print("🔲 Generating QR code...")
            qr_path = self.output_dir / f'{filename}_qr_{timestamp}.png'
            self.generate_qr_code(summary, str(qr_path))
            results['qr_code_path'] = str(qr_path)
            print(f"✓ QR code saved to {qr_path}")
            
            # Step 4: Convert to PDF
            print("📑 Converting Word to PDF...")
            temp_pdf = self.output_dir / f'{filename}_temp_{timestamp}.pdf'
            self.convert_docx_to_pdf(docx_path, str(temp_pdf))
            print("✓ PDF conversion complete")
            
            # Step 5: Add QR code to PDF
            print("🎨 Adding QR code to PDF header...")
            final_pdf = self.output_dir / f'{filename}_final_{timestamp}.pdf'
            self.add_qr_to_pdf_header(str(temp_pdf), str(qr_path), str(final_pdf))
            results['final_pdf_path'] = str(final_pdf)
            print(f"✓ Final PDF created: {final_pdf}")
            
            # Clean up temp file
            if temp_pdf.exists():
                temp_pdf.unlink()
            
            # Step 6: Send email
            if send_email and recipient_email:
                print("📧 Sending email...")
                self.send_email(str(final_pdf), recipient_email, summary)
                results['email_sent'] = True
                print(f"✓ Email sent to {recipient_email}")
            
            results['success'] = True
            print("\n✅ Document processing complete!")
            
        except Exception as e:
            results['error'] = str(e)
            print(f"\n❌ Error: {e}")
        
        return results


def load_config(config_path: str = 'config.json') -> Dict[str, Any]:
    """Load configuration from JSON file"""
    if Path(config_path).exists():
        with open(config_path, 'r') as f:
            return json.load(f)
    return {}


def save_config(config: Dict[str, Any], config_path: str = 'config.json'):
    """Save configuration to JSON file"""
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)


if __name__ == '__main__':
    # Example usage
    print("Document Automation Script")
    print("=" * 50)
    
    # Load or create config
    config = load_config()
    
    if not config.get('gemini_api_key'):
        print("\nConfiguration needed. Please run the Streamlit dashboard or edit config.json")
        print("Required fields:")
        print("  - gemini_api_key: Your Google Gemini API key")
        print("  - email.sender: Your email address")
        print("  - email.password: Your email password/app password")
        exit(1)
    
    # Initialize automation
    automation = DocumentAutomation(config)
    
    # Process a document
    docx_file = input("\nEnter path to Word document: ")
    recipient = input("Enter recipient email (or press Enter to skip): ")
    
    results = automation.process_document(
        docx_file,
        recipient_email=recipient if recipient else None,
        send_email=bool(recipient)
    )
    
    print("\n" + "=" * 50)
    print("Results:", json.dumps(results, indent=2))
