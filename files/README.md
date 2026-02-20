# Document Automation System 📄⚖️

Sistema de automação para processamento de documentos jurídicos com IA, geração de QR codes e conversão para PDF.

[English](#english) | [Português](#português)

---

## Português 🇧🇷

### 🎯 Funcionalidades

Este sistema automatiza completamente o processamento de documentos jurídicos:

1. **📄 Extração de Texto** - Lê automaticamente o conteúdo de documentos Word
2. **🤖 Resumo com IA** - Gera resumos inteligentes usando Google Gemini
3. **🔲 QR Code** - Cria QR codes contendo o resumo do documento
4. **📑 Conversão PDF** - Converte documentos Word para PDF profissional
5. **🎨 Inserção Automática** - Adiciona QR code no cabeçalho do PDF com etiqueta "Resumo"
6. **📧 Envio por Email** - Envia o documento final automaticamente (opcional)

### 🖥️ Interface

O sistema inclui um **dashboard Streamlit** profissional e intuitivo:

- ✅ Interface web moderna e responsiva
- ✅ Upload de documentos por drag-and-drop
- ✅ Visualização em tempo real do progresso
- ✅ Histórico completo de processamentos
- ✅ Download direto dos PDFs gerados
- ✅ Configuração visual de todas as opções

### 📋 Pré-requisitos

#### Software Necessário:

1. **Python 3.8 ou superior**
   - Download: https://www.python.org/downloads/
   - Durante instalação, marque "Add Python to PATH"

2. **LibreOffice** (para conversão Word → PDF)
   - Download: https://www.libreoffice.org/download/
   - Instale a versão completa (não apenas Viewer)

3. **Google Gemini API Key** (gratuita)
   - Obtenha em: https://makersuite.google.com/app/apikey
   - Requer conta Google

#### Configurações de Email (Opcional):

Para envio automático de emails, você precisará:
- Endereço de email (Gmail recomendado)
- **App Password** (não use sua senha normal!)
  - Gmail: https://myaccount.google.com/apppasswords
  - Outlook: Configure nas configurações de segurança

### 🚀 Instalação

#### Passo 1: Clone ou baixe os arquivos

```bash
# Clone o repositório (se disponível)
git clone <repository-url>
cd document-automation

# OU baixe os arquivos manualmente e extraia
```

#### Passo 2: Instale as dependências Python

Abra o terminal/prompt de comando na pasta do projeto e execute:

```bash
pip install -r requirements.txt
```

**Nota para Windows:** Se encontrar erros, tente:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

#### Passo 3: Verifique a instalação do LibreOffice

Teste se o LibreOffice está instalado corretamente:

```bash
# Windows
soffice --version

# Mac/Linux
libreoffice --version
```

Se o comando não funcionar, adicione o LibreOffice ao PATH do sistema.

### 📖 Como Usar

#### Opção 1: Dashboard Streamlit (Recomendado)

1. **Inicie o dashboard:**

```bash
streamlit run streamlit_app.py
```

2. **O navegador abrirá automaticamente** em `http://localhost:8501`

3. **Configure na barra lateral:**
   - Insira sua Gemini API Key
   - Configure email (se quiser envio automático)
   - Defina pasta de saída (opcional)

4. **Processe documentos:**
   - Vá para aba "Processar Documento"
   - Faça upload de um arquivo .docx
   - Escolha se quer enviar por email
   - Clique em "Processar Documento"
   - Aguarde o processamento (você verá o progresso)
   - Baixe o PDF final ou visualize no histórico

#### Opção 2: Linha de Comando

1. **Configure o arquivo config.json:**

```json
{
  "gemini_api_key": "SUA_API_KEY_AQUI",
  "output_dir": "output",
  "email": {
    "sender": "seu-email@gmail.com",
    "password": "sua-app-password",
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587
  }
}
```

2. **Execute o script:**

```bash
python document_automation.py
```

3. **Siga as instruções** no terminal

### 📁 Estrutura de Arquivos

```
document-automation/
├── streamlit_app.py          # Dashboard web
├── document_automation.py    # Script principal de automação
├── requirements.txt          # Dependências Python
├── config.json              # Arquivo de configuração (criado no primeiro uso)
├── output/                  # PDFs e QR codes gerados
├── temp/                    # Arquivos temporários
└── README.md               # Este arquivo
```

### 🔧 Solução de Problemas

#### Erro: "LibreOffice not found"
- **Solução:** Instale o LibreOffice e adicione ao PATH
- **Windows:** Adicione `C:\Program Files\LibreOffice\program` ao PATH
- **Mac:** LibreOffice normalmente já está no PATH após instalação
- **Linux:** `sudo apt-get install libreoffice`

#### Erro: "Gemini API error"
- **Solução:** Verifique se sua API key está correta
- Teste em: https://makersuite.google.com/
- Certifique-se de não ter atingido o limite de requisições gratuitas

#### Erro: "Email sending failed"
- **Solução:** Use App Password, não sua senha normal
- Gmail: Ative verificação em 2 etapas primeiro
- Outlook: Permita "aplicativos menos seguros" ou use App Password

#### Erro: "Module not found"
- **Solução:** Instale novamente as dependências
```bash
pip install -r requirements.txt --upgrade
```

### 💡 Dicas de Uso

1. **Organize seus documentos:** Mantenha templates Word com cabeçalho/rodapé já formatados
2. **QR Codes:** Funciona melhor com resumos de até 500 caracteres
3. **Email em lote:** Processe vários documentos de uma vez usando o script Python
4. **Backup:** Os arquivos originais nunca são modificados
5. **Histórico:** O dashboard mantém histórico completo de processamentos

### 📊 Limites e Custos

- **Gemini API:** Gratuito até 60 requisições/minuto
- **QR Server API:** Completamente gratuito, sem limites
- **Email:** Sem custos adicionais
- **Armazenamento:** Apenas espaço local no seu computador

### 🔒 Segurança

- **API Keys:** Armazenadas apenas localmente no seu computador
- **Senhas:** Use sempre App Passwords, nunca senhas principais
- **Dados:** Nenhum dado é enviado para servidores externos (exceto APIs necessárias)
- **Documentos:** Processados localmente, não são armazenados em nuvem

---

## English 🇺🇸

### 🎯 Features

This system fully automates legal document processing:

1. **📄 Text Extraction** - Automatically reads Word document content
2. **🤖 AI Summary** - Generates intelligent summaries using Google Gemini
3. **🔲 QR Code** - Creates QR codes containing the document summary
4. **📑 PDF Conversion** - Converts Word documents to professional PDFs
5. **🎨 Automatic Insertion** - Adds QR code to PDF header with "Resumo" label
6. **📧 Email Delivery** - Automatically sends final document (optional)

### 🖥️ Interface

The system includes a professional and intuitive **Streamlit dashboard**:

- ✅ Modern, responsive web interface
- ✅ Drag-and-drop document upload
- ✅ Real-time progress tracking
- ✅ Complete processing history
- ✅ Direct PDF downloads
- ✅ Visual configuration of all options

### 📋 Prerequisites

#### Required Software:

1. **Python 3.8 or higher**
   - Download: https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"

2. **LibreOffice** (for Word → PDF conversion)
   - Download: https://www.libreoffice.org/download/
   - Install full version (not just Viewer)

3. **Google Gemini API Key** (free)
   - Get it at: https://makersuite.google.com/app/apikey
   - Requires Google account

#### Email Settings (Optional):

For automatic email sending, you'll need:
- Email address (Gmail recommended)
- **App Password** (don't use your regular password!)
  - Gmail: https://myaccount.google.com/apppasswords
  - Outlook: Configure in security settings

### 🚀 Installation

#### Step 1: Clone or download files

```bash
# Clone repository (if available)
git clone <repository-url>
cd document-automation

# OR download files manually and extract
```

#### Step 2: Install Python dependencies

Open terminal/command prompt in project folder and run:

```bash
pip install -r requirements.txt
```

**Windows Note:** If you encounter errors, try:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 3: Verify LibreOffice installation

Test if LibreOffice is installed correctly:

```bash
# Windows
soffice --version

# Mac/Linux
libreoffice --version
```

If command doesn't work, add LibreOffice to system PATH.

### 📖 How to Use

#### Option 1: Streamlit Dashboard (Recommended)

1. **Start the dashboard:**

```bash
streamlit run streamlit_app.py
```

2. **Browser will open automatically** at `http://localhost:8501`

3. **Configure in sidebar:**
   - Enter your Gemini API Key
   - Configure email (if you want automatic sending)
   - Set output folder (optional)

4. **Process documents:**
   - Go to "Process Document" tab
   - Upload a .docx file
   - Choose if you want to send by email
   - Click "Process Document"
   - Wait for processing (you'll see progress)
   - Download final PDF or view in history

#### Option 2: Command Line

1. **Configure config.json file:**

```json
{
  "gemini_api_key": "YOUR_API_KEY_HERE",
  "output_dir": "output",
  "email": {
    "sender": "your-email@gmail.com",
    "password": "your-app-password",
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587
  }
}
```

2. **Run the script:**

```bash
python document_automation.py
```

3. **Follow instructions** in terminal

### 🔧 Troubleshooting

#### Error: "LibreOffice not found"
- **Solution:** Install LibreOffice and add to PATH
- **Windows:** Add `C:\Program Files\LibreOffice\program` to PATH
- **Mac:** LibreOffice usually in PATH after installation
- **Linux:** `sudo apt-get install libreoffice`

#### Error: "Gemini API error"
- **Solution:** Check if your API key is correct
- Test at: https://makersuite.google.com/
- Make sure you haven't hit the free tier limit

#### Error: "Email sending failed"
- **Solution:** Use App Password, not your regular password
- Gmail: Enable 2-step verification first
- Outlook: Allow "less secure apps" or use App Password

#### Error: "Module not found"
- **Solution:** Reinstall dependencies
```bash
pip install -r requirements.txt --upgrade
```

### 💡 Usage Tips

1. **Organize documents:** Keep Word templates with header/footer already formatted
2. **QR Codes:** Works best with summaries up to 500 characters
3. **Batch email:** Process multiple documents at once using Python script
4. **Backup:** Original files are never modified
5. **History:** Dashboard maintains complete processing history

### 📊 Limits and Costs

- **Gemini API:** Free up to 60 requests/minute
- **QR Server API:** Completely free, no limits
- **Email:** No additional costs
- **Storage:** Only local space on your computer

### 🔒 Security

- **API Keys:** Stored only locally on your computer
- **Passwords:** Always use App Passwords, never main passwords
- **Data:** No data sent to external servers (except necessary APIs)
- **Documents:** Processed locally, not stored in cloud

---

## 📝 License

This project is for educational and professional use. Please ensure compliance with all applicable data protection regulations when processing legal documents.

## 🤝 Support

For issues or questions:
1. Check troubleshooting section above
2. Verify all prerequisites are installed
3. Check configuration in sidebar/config.json
4. Review error logs in history tab

---

**Version 1.0** | Developed for legal document automation
