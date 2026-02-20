"""
Streamlit Dashboard for Document Automation
A professional interface for processing legal documents with QR codes
"""

import streamlit as st
import json
import os
from pathlib import Path
from datetime import datetime
import sys

# Import our automation script
from document_automation import DocumentAutomation, load_config, save_config

# Page configuration
st.set_page_config(
    page_title="Document Automation",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1e3a8a;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #64748b;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1fae5;
        border-left: 4px solid #10b981;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #fee2e2;
        border-left: 4px solid #ef4444;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #dbeafe;
        border-left: 4px solid #3b82f6;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #f8fafc;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e2e8f0;
    }
    .stButton>button {
        width: 100%;
        background-color: #1e3a8a;
        color: white;
        font-weight: 600;
        padding: 0.75rem;
        border-radius: 0.5rem;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #1e40af;
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'config' not in st.session_state:
    st.session_state.config = load_config()
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'results' not in st.session_state:
    st.session_state.results = []


def main():
    """Main application"""
    
    # Header
    st.markdown('<div class="main-header">⚖️ Document Automation System</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Automatize o processamento de documentos jurídicos com IA</div>', unsafe_allow_html=True)
    
    # Sidebar - Configuration
    with st.sidebar:
        st.header("⚙️ Configurações")
        
        with st.expander("🔑 API Keys", expanded=not st.session_state.config.get('gemini_api_key')):
            gemini_key = st.text_input(
                "Gemini API Key",
                value=st.session_state.config.get('gemini_api_key', ''),
                type="password",
                help="Obtenha sua chave em: https://makersuite.google.com/app/apikey"
            )
            
            if gemini_key != st.session_state.config.get('gemini_api_key', ''):
                st.session_state.config['gemini_api_key'] = gemini_key
            
            # CloudConvert for cloud deployment (optional for local)
            cloudconvert_key = st.text_input(
                "CloudConvert API Key (para nuvem)",
                value=st.session_state.config.get('cloudconvert_api_key', ''),
                type="password",
                help="Necessário para Streamlit Cloud. Gratuito: https://cloudconvert.com/register (25 conversões/dia)"
            )
            
            if cloudconvert_key != st.session_state.config.get('cloudconvert_api_key', ''):
                st.session_state.config['cloudconvert_api_key'] = cloudconvert_key
        
        with st.expander("📧 Configurações de Email", expanded=False):
            email_sender = st.text_input(
                "Seu Email",
                value=st.session_state.config.get('email', {}).get('sender', ''),
                help="Email que enviará os documentos"
            )
            
            email_password = st.text_input(
                "Senha/App Password",
                value=st.session_state.config.get('email', {}).get('password', ''),
                type="password",
                help="Use App Password para Gmail"
            )
            
            smtp_server = st.text_input(
                "Servidor SMTP",
                value=st.session_state.config.get('email', {}).get('smtp_server', 'smtp.gmail.com'),
                help="smtp.gmail.com para Gmail"
            )
            
            smtp_port = st.number_input(
                "Porta SMTP",
                value=st.session_state.config.get('email', {}).get('smtp_port', 587),
                min_value=1,
                max_value=65535
            )
            
            if any([email_sender, email_password, smtp_server]):
                if 'email' not in st.session_state.config:
                    st.session_state.config['email'] = {}
                st.session_state.config['email'].update({
                    'sender': email_sender,
                    'password': email_password,
                    'smtp_server': smtp_server,
                    'smtp_port': smtp_port
                })
        
        with st.expander("📁 Configurações Gerais", expanded=False):
            output_dir = st.text_input(
                "Diretório de Saída",
                value=st.session_state.config.get('output_dir', 'output'),
                help="Pasta onde os arquivos serão salvos"
            )
            st.session_state.config['output_dir'] = output_dir
        
        # Save configuration
        if st.button("💾 Salvar Configurações", use_container_width=True):
            save_config(st.session_state.config)
            st.success("✓ Configurações salvas!")
        
        # Check configuration status
        st.divider()
        st.subheader("Status da Configuração")
        
        config_status = {
            "Gemini API": bool(st.session_state.config.get('gemini_api_key')),
            "CloudConvert API": bool(st.session_state.config.get('cloudconvert_api_key')),
            "Email Config": bool(st.session_state.config.get('email', {}).get('sender')),
        }
        
        for item, status in config_status.items():
            if status:
                st.success(f"✓ {item}")
            else:
                st.warning(f"⚠ {item}")
    
    # Main content area
    tab1, tab2, tab3 = st.tabs(["📤 Processar Documento", "📊 Histórico", "ℹ️ Sobre"])
    
    # Tab 1: Process Document
    with tab1:
        # Check if configuration is ready
        if not st.session_state.config.get('gemini_api_key'):
            st.markdown('<div class="error-box">⚠️ Configure a API Key do Gemini na barra lateral para começar.</div>', unsafe_allow_html=True)
            return
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📄 Upload do Documento")
            
            uploaded_file = st.file_uploader(
                "Selecione um documento Word (.docx)",
                type=['docx'],
                help="Faça upload do documento jurídico que deseja processar"
            )
            
            if uploaded_file:
                # Save uploaded file temporarily
                temp_dir = Path("temp")
                temp_dir.mkdir(exist_ok=True)
                temp_path = temp_dir / uploaded_file.name
                
                with open(temp_path, 'wb') as f:
                    f.write(uploaded_file.getbuffer())
                
                st.success(f"✓ Arquivo carregado: {uploaded_file.name}")
                
                # File info
                file_size = uploaded_file.size / 1024  # KB
                st.info(f"📊 Tamanho: {file_size:.2f} KB")
        
        with col2:
            st.subheader("📧 Opções de Envio")
            
            send_email = st.checkbox(
                "Enviar por email",
                value=True,
                help="Enviar o PDF final por email"
            )
            
            recipient_email = ""
            if send_email:
                recipient_email = st.text_input(
                    "Email do destinatário",
                    placeholder="exemplo@email.com",
                    help="Email para enviar o documento processado"
                )
                
                if not st.session_state.config.get('email', {}).get('sender'):
                    st.warning("⚠️ Configure o email na barra lateral")
        
        # Process button
        st.divider()
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            if uploaded_file:
                if st.button("🚀 Processar Documento", use_container_width=True):
                    process_document(temp_path, recipient_email if send_email else None, send_email)
    
    # Tab 2: History
    with tab2:
        st.subheader("📊 Histórico de Processamento")
        
        if st.session_state.results:
            for i, result in enumerate(reversed(st.session_state.results)):
                with st.expander(
                    f"{'✅' if result['success'] else '❌'} {Path(result['input_file']).name} - {result['timestamp'][:19]}",
                    expanded=(i == 0)
                ):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Arquivo:**", Path(result['input_file']).name)
                        st.write("**Status:**", "✅ Sucesso" if result['success'] else "❌ Erro")
                        st.write("**Data:**", result['timestamp'][:19])
                    
                    with col2:
                        if result['success']:
                            if 'text_length' in result:
                                st.write("**Texto extraído:**", f"{result['text_length']} caracteres")
                            if 'email_sent' in result:
                                st.write("**Email:**", "✅ Enviado" if result['email_sent'] else "❌ Não enviado")
                    
                    if result['success'] and 'summary' in result:
                        st.write("**Resumo:**")
                        st.info(result['summary'])
                        
                        if 'final_pdf_path' in result and Path(result['final_pdf_path']).exists():
                            with open(result['final_pdf_path'], 'rb') as f:
                                st.download_button(
                                    "⬇️ Baixar PDF",
                                    f.read(),
                                    file_name=Path(result['final_pdf_path']).name,
                                    mime="application/pdf"
                                )
                        
                        if 'qr_code_path' in result and Path(result['qr_code_path']).exists():
                            st.image(result['qr_code_path'], caption="QR Code Gerado", width=200)
                    
                    if not result['success'] and 'error' in result:
                        st.error(f"Erro: {result['error']}")
        else:
            st.info("Nenhum documento processado ainda. Faça upload de um documento na aba 'Processar Documento'.")
    
    # Tab 3: About
    with tab3:
        st.subheader("ℹ️ Sobre o Sistema")
        
        st.markdown("""
        ### 🎯 Funcionalidades
        
        Este sistema automatiza o processamento de documentos jurídicos com as seguintes etapas:
        
        1. **📄 Extração de Texto**: Lê o conteúdo do documento Word
        2. **🤖 Resumo com IA**: Gera um resumo conciso usando Google Gemini
        3. **🔲 QR Code**: Cria um QR code contendo o resumo
        4. **📑 Conversão PDF**: Converte o documento para PDF
        5. **🎨 Inserção**: Adiciona o QR code no cabeçalho do PDF
        6. **📧 Envio**: Envia o documento final por email (opcional)
        
        ### 🔧 Requisitos
        
        - **Python 3.8+**
        - **LibreOffice** (para conversão Word → PDF)
        - **Gemini API Key** (gratuita)
        - **Email configurado** (opcional, para envio automático)
        
        ### 📚 Tecnologias
        
        - **Streamlit**: Interface web
        - **Google Gemini**: Geração de resumos com IA
        - **QR Server API**: Geração de QR codes (gratuita)
        - **python-docx**: Leitura de documentos Word
        - **PyPDF2 & ReportLab**: Manipulação de PDFs
        
        ### 🆘 Suporte
        
        Para problemas ou dúvidas:
        - Verifique as configurações na barra lateral
        - Certifique-se de que o LibreOffice está instalado
        - Confira os logs de erro no histórico
        
        ---
        
        **Versão 1.0** | Desenvolvido para automação de documentos jurídicos
        """)


def process_document(docx_path: Path, recipient_email: str, send_email: bool):
    """Process document with progress tracking"""
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Initialize automation
        status_text.text("🔧 Inicializando sistema...")
        progress_bar.progress(10)
        
        automation = DocumentAutomation(st.session_state.config)
        
        # Step 1: Extract text
        status_text.text("📄 Extraindo texto do documento...")
        progress_bar.progress(20)
        text = automation.extract_text_from_docx(str(docx_path))
        
        # Step 2: Generate summary
        status_text.text("🤖 Gerando resumo com Gemini AI...")
        progress_bar.progress(40)
        summary = automation.summarize_with_gemini(text)
        
        # Step 3: Generate QR code
        status_text.text("🔲 Gerando QR code...")
        progress_bar.progress(55)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        qr_path = Path(st.session_state.config.get('output_dir', 'output')) / f'{docx_path.stem}_qr_{timestamp}.png'
        automation.generate_qr_code(summary, str(qr_path))
        
        # Step 4: Convert to PDF
        status_text.text("📑 Convertendo para PDF...")
        progress_bar.progress(70)
        temp_pdf = Path(st.session_state.config.get('output_dir', 'output')) / f'{docx_path.stem}_temp_{timestamp}.pdf'
        automation.convert_docx_to_pdf(str(docx_path), str(temp_pdf))
        
        # Step 5: Add QR to PDF
        status_text.text("🎨 Adicionando QR code ao PDF...")
        progress_bar.progress(85)
        final_pdf = Path(st.session_state.config.get('output_dir', 'output')) / f'{docx_path.stem}_final_{timestamp}.pdf'
        automation.add_qr_to_pdf_header(str(temp_pdf), str(qr_path), str(final_pdf))
        
        # Clean up temp file
        if temp_pdf.exists():
            temp_pdf.unlink()
        
        # Step 6: Send email (optional)
        email_sent = False
        if send_email and recipient_email:
            status_text.text("📧 Enviando email...")
            progress_bar.progress(95)
            automation.send_email(str(final_pdf), recipient_email, summary)
            email_sent = True
        
        progress_bar.progress(100)
        status_text.text("✅ Processamento concluído!")
        
        # Store results
        result = {
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'input_file': str(docx_path),
            'text_length': len(text),
            'summary': summary,
            'qr_code_path': str(qr_path),
            'final_pdf_path': str(final_pdf),
            'email_sent': email_sent
        }
        st.session_state.results.append(result)
        
        # Display success message
        st.markdown('<div class="success-box">✅ <strong>Documento processado com sucesso!</strong></div>', unsafe_allow_html=True)
        
        # Show summary
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📝 Resumo Gerado")
            st.info(summary)
        
        with col2:
            st.subheader("🔲 QR Code")
            st.image(str(qr_path), width=250)
        
        # Download button
        with open(final_pdf, 'rb') as f:
            st.download_button(
                "⬇️ Baixar PDF Final",
                f.read(),
                file_name=final_pdf.name,
                mime="application/pdf",
                use_container_width=True
            )
        
        if email_sent:
            st.success(f"📧 Email enviado para: {recipient_email}")
        
    except Exception as e:
        progress_bar.progress(100)
        status_text.text("❌ Erro no processamento")
        
        st.markdown(f'<div class="error-box">❌ <strong>Erro:</strong> {str(e)}</div>', unsafe_allow_html=True)
        
        # Store error result
        result = {
            'success': False,
            'timestamp': datetime.now().isoformat(),
            'input_file': str(docx_path),
            'error': str(e)
        }
        st.session_state.results.append(result)
        
        # Show troubleshooting tips
        with st.expander("🔍 Dicas de Solução"):
            st.markdown("""
            **Erros comuns e soluções:**
            
            - **Erro de conversão PDF**: Instale o LibreOffice
            - **Erro Gemini API**: Verifique sua API key
            - **Erro de email**: Verifique credenciais e use App Password para Gmail
            - **Erro QR Code**: Verifique conexão com internet
            """)


if __name__ == '__main__':
    main()
