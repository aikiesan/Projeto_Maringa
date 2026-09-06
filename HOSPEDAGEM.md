# Hospedagem do painel

O painel é um arquivo estático único, com todos os dados embutidos. Não precisa
de servidor, de banco no ar nem de build remoto.

`python -m tools.build_site` gera três saídas:

| Arquivo | Conteúdo | Onde vai |
|---|---|---|
| `index.html` | painel completo, **com pontos focais nominais** | abrir localmente |
| `public/index.html` | idêntico ao anterior | diretório de saída da hospedagem |
| `site/artifact.html` | só a camada anonimizada, **sem contatos** | publicação como Artifact |

## Regra que não se negocia

`index.html` e `public/index.html` trazem nome, cargo, e-mail e telefone de 24
pontos focais — e várias dessas pessoas são as mesmas que aparecem no corpus como
`ENT-0xx`. Cruzar as duas tabelas reidentifica entrevistado.

**Essas duas saídas só podem ser servidas atrás de autenticação.** Sem controle de
acesso, use `site/artifact.html`, que não tem contatos.

## Cloudflare Pages + Access (gratuito)

1. **Pages** → *Create a project* → *Connect to Git* → autorize o GitHub App e
   escolha `aikiesan/Projeto_Maringa`. Repositório privado é suportado.
2. Configuração de build:
   - *Framework preset*: **None**
   - *Build command*: **deixar vazio**
   - *Build output directory*: **`public`**

   O diretório de saída é o que fica público. Apontar para a raiz publicaria
   `codebook/`, `data/contacts.json` e o código — exatamente o que não pode.
3. Deploy. A cada `git push` no `main` o painel é reconstruído.
4. **Zero Trust** → *Access* → *Applications* → *Add an application* →
   *Self-hosted*, apontando para o domínio do projeto (`<projeto>.pages.dev`).
5. Política: *Action* **Allow**, *Include* → **Emails** → os e-mails que podem
   entrar. O plano gratuito cobre até 50 usuários.
6. Teste numa janela anônima: deve pedir o código enviado por e-mail antes de
   servir qualquer conteúdo.

Enquanto o Access não estiver configurado e testado, o deploy fica público.
Configure o Access **antes** de compartilhar o link.

## Alternativas consideradas

- **Vercel / Netlify (free)**: aceitam repositório privado, mas proteção por senha
  é recurso pago (Vercel Pro US$ 20/mês; Netlify em plano pago). O Hobby da Vercel
  ainda veda uso comercial.
- **Railway**: orientado a contêiner — cobra pelo tempo de execução para servir um
  arquivo estático, e o plano gratuito dá US$ 1 de crédito por mês. Deploy nasce
  público.
- **GitHub Pages**: com repositório privado exige GitHub Pro, e o site publicado
  continua público. Controle de acesso só no Enterprise.
- **Tailscale**: serve o painel do próprio computador pela rede privada, sem nada
  hospedado. Melhor opção se você preferir não pôr os contatos em terceiros — o
  custo é que a outra pessoa precisa instalar o cliente.

## Se um dia o painel for aberto

Antes de qualquer publicação sem autenticação, duas coisas precisam mudar:
retirar a seção de pontos focais da saída pública (o `tools/project_base.py` já
isola essa seção) e limpar do histórico do git as planilhas removidas em
`358b86e`, que continuam recuperáveis nos commits de julho.
