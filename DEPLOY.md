# 🚀 Guia de Deploy - Amazon Fruit

Este guia fornece instruções detalhadas para fazer deploy da aplicação Amazon Fruit em diferentes plataformas.

## 📋 Índice

- [Pré-requisitos](#pré-requisitos)
- [Variáveis de Ambiente](#variáveis-de-ambiente)
- [Deploy na Vercel](#deploy-na-vercel)
- [Deploy com Docker](#deploy-com-docker)
- [Deploy no Railway](#deploy-no-railway)
- [Deploy no Netlify](#deploy-no-netlify)
- [Monitoramento](#monitoramento)

---

## ✅ Pré-requisitos

Antes de fazer o deploy, certifique-se de que:

- ✅ Todos os testes estão passando: `npm test`
- ✅ Build está funcionando: `npm run build`
- ✅ Linting está limpo: `npm run lint`
- ✅ Type-check está passando: `npm run type-check`

## 🔐 Variáveis de Ambiente

### Variáveis Obrigatórias

\`\`\`env
# API Backend
NEXT_PUBLIC_API_URL=https://api.amazon-fruit.com

# Aplicação
NEXT_PUBLIC_APP_NAME=Amazon Fruit
NEXT_PUBLIC_APP_URL=https://amazon-fruit.vercel.app
\`\`\`

### Variáveis Opcionais

\`\`\`env
# Analytics (opcional)
NEXT_PUBLIC_GA_TRACKING_ID=G-XXXXXXXXXX

# Sentry (opcional)
NEXT_PUBLIC_SENTRY_DSN=https://xxx@sentry.io/xxx
\`\`\`

---

## 🟢 Deploy na Vercel (Recomendado)

A Vercel é a plataforma recomendada para Next.js.

### 1. Via Interface Web

1. Acesse [vercel.com](https://vercel.com)
2. Faça login com GitHub
3. Clique em "New Project"
4. Importe o repositório `amazon-fruit`
5. Configure as variáveis de ambiente
6. Clique em "Deploy"

### 2. Via CLI

\`\`\`bash
# Instalar Vercel CLI
npm i -g vercel

# Fazer login
vercel login

# Deploy
vercel

# Deploy para produção
vercel --prod
\`\`\`

### 3. Configuração de Domínio

1. No dashboard da Vercel, vá em "Settings" > "Domains"
2. Adicione seu domínio customizado
3. Configure DNS conforme instruções

### 4. Configurações Recomendadas

- **Framework Preset**: Next.js
- **Build Command**: `npm run build`
- **Output Directory**: `.next`
- **Install Command**: `npm ci`
- **Node Version**: 20.x

---

## 🐳 Deploy com Docker

### Produção Local

\`\`\`bash
# Build da imagem
docker build -t amazon-fruit:latest .

# Executar container
docker run -p 3000:3000 \\
  -e NEXT_PUBLIC_API_URL=https://api.amazon-fruit.com \\
  amazon-fruit:latest
\`\`\`

### Docker Compose

\`\`\`bash
# Criar arquivo .env.production
cp .env.example .env.production

# Editar variáveis
nano .env.production

# Iniciar serviços
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar serviços
docker-compose down
\`\`\`

### Deploy em Cloud com Docker

#### AWS ECS

\`\`\`bash
# Build e push para ECR
aws ecr get-login-password --region us-east-1 | \\
  docker login --username AWS --password-stdin xxx.dkr.ecr.us-east-1.amazonaws.com

docker build -t amazon-fruit .
docker tag amazon-fruit:latest xxx.dkr.ecr.us-east-1.amazonaws.com/amazon-fruit:latest
docker push xxx.dkr.ecr.us-east-1.amazonaws.com/amazon-fruit:latest
\`\`\`

#### Google Cloud Run

\`\`\`bash
# Build e deploy
gcloud builds submit --tag gcr.io/PROJECT-ID/amazon-fruit
gcloud run deploy amazon-fruit --image gcr.io/PROJECT-ID/amazon-fruit --platform managed
\`\`\`

---

## 🚂 Deploy no Railway

Railway oferece deploy simples com Docker.

### 1. Via Interface

1. Acesse [railway.app](https://railway.app)
2. Faça login com GitHub
3. Clique em "New Project"
4. Selecione "Deploy from GitHub repo"
5. Escolha `amazon-fruit`
6. Railway detecta automaticamente o Dockerfile
7. Configure as variáveis de ambiente
8. Deploy automático!

### 2. Via CLI

\`\`\`bash
# Instalar Railway CLI
npm i -g @railway/cli

# Login
railway login

# Inicializar projeto
railway init

# Deploy
railway up

# Abrir no navegador
railway open
\`\`\`

### 3. Configuração

- **Start Command**: Automático (usa CMD do Dockerfile)
- **Port**: 3000
- **Health Check**: `/`

---

## 🌐 Deploy no Netlify

### 1. Via Interface

1. Acesse [netlify.com](https://netlify.com)
2. Clique em "Add new site" > "Import an existing project"
3. Conecte com GitHub
4. Selecione o repositório
5. Configure:
   - **Build command**: `npm run build`
   - **Publish directory**: `.next`
   - **Base directory**: (vazio)
6. Adicione variáveis de ambiente
7. Deploy!

### 2. Via CLI

\`\`\`bash
# Instalar Netlify CLI
npm i -g netlify-cli

# Login
netlify login

# Deploy
netlify deploy --prod
\`\`\`

### 3. Configuração netlify.toml

\`\`\`toml
[build]
  command = "npm run build"
  publish = ".next"

[build.environment]
  NODE_VERSION = "20"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
\`\`\`

---

## 📊 Monitoramento

### Vercel Analytics

Habilite no dashboard da Vercel:
- Settings > Analytics > Enable

### Sentry (Error Tracking)

\`\`\`bash
npm install @sentry/nextjs
npx @sentry/wizard@latest -i nextjs
\`\`\`

Configure no `.env`:

\`\`\`env
NEXT_PUBLIC_SENTRY_DSN=https://xxx@sentry.io/xxx
\`\`\`

### Google Analytics

Adicione no `layout.tsx`:

\`\`\`typescript
import Script from 'next/script';

export default function RootLayout({ children }) {
  return (
    <html>
      <head>
        <Script
          src={\`https://www.googletagmanager.com/gtag/js?id=\${process.env.NEXT_PUBLIC_GA_TRACKING_ID}\`}
          strategy="afterInteractive"
        />
        <Script id="google-analytics" strategy="afterInteractive">
          {\`
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', '\${process.env.NEXT_PUBLIC_GA_TRACKING_ID}');
          \`}
        </Script>
      </head>
      <body>{children}</body>
    </html>
  );
}
\`\`\`

---

## 🔄 CI/CD

O projeto já inclui GitHub Actions configurado (`.github/workflows/ci.yml`):

- ✅ Executa testes
- ✅ Verifica linting
- ✅ Type-check
- ✅ Build
- ✅ Build Docker

### Deploy Automático

Configure deploy automático:

**Vercel**: Automático após push para `main`  
**Railway**: Configure webhook no dashboard  
**Netlify**: Automático após push para `main`

---

## 🚨 Troubleshooting

### Build falha

\`\`\`bash
# Limpar cache
rm -rf .next node_modules
npm install
npm run build
\`\`\`

### Variáveis de ambiente não funcionam

- Certifique-se de usar `NEXT_PUBLIC_` para variáveis do client
- Reinicie o servidor após alterar `.env`
- No deploy, configure no painel da plataforma

### Erro de memória no build

Aumente limite de memória:

\`\`\`json
{
  "scripts": {
    "build": "NODE_OPTIONS='--max-old-space-size=4096' next build"
  }
}
\`\`\`

---

## ✅ Checklist de Deploy

- [ ] Testes passando
- [ ] Build local funcionando
- [ ] Variáveis de ambiente configuradas
- [ ] Domínio configurado (se aplicável)
- [ ] SSL/HTTPS ativo
- [ ] Monitoramento configurado
- [ ] Backups configurados
- [ ] Documentação atualizada

---

## 📞 Suporte

Para problemas ou dúvidas:

- 📧 Email: suporte@amazon-fruit.com
- 💬 GitHub Issues: [github.com/seu-usuario/amazon-fruit/issues](https://github.com/seu-usuario/amazon-fruit/issues)
- 📚 Documentação: [docs/](docs/)

---

<div align="center">
  <strong>Deploy bem-sucedido! 🎉</strong>
</div>
