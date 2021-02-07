# Video Dataset Creator #

O escopo desse projeto de programação de final é o design,  desenvolvimento e documentação de __crawlers__, com funcões como continuar downloads caso interrompidos, e com capacidade para execução por longos periodos de tempo. Para isso, serão criadas três variações com fins específicos: 
 - Busca e coleta de vídeos a partir de termos de pesquisa.
 - Coleta de vídeos a partir de links.
 - Coleta de vídeos a partir de uma API.
São suportadas duas plataformas de hospedagem de vídeos: [Youtube](https://www.youtube.com/) e [Video@RNP](http://www.videoaula.rnp.br/portal/home). Esses _crawlers_} também terão interação através de interface em linhas de comando, dadas suas funções pontuais e execução majoritariamente em servidores _headless_} (sem interface gráfica).

Cada ferramenta foi implementada utilizando a linguagem Python (Versão 3.6.12), utilizando o gerenciador de pacotes Pipenv (versão 2020.11.15), que torna a instalação das ferramentas e dependências mais conveniente.

Mais detalhes da modelagem e desenvolvimento dessas ferramentas podem ser encontradas no [Relatório](https://github.com/pedropva/video-dataset-creator/blob/main/video-dataset-creator-relatorio.pdf)

O projeto contém dois diretórios: _docs_, que contém os arquivos para geração da documentação do projeto, e crawlers, esta, por sua vez é divida em três módulos: 

- rnp: Contém o crawler focado na plataforma Video@RNP.
- tests: Contém os testes unitários automatizados para todos os crawlers.
- youtube: Contém os crawlers para download de videos na plataforma youtube a partir de busca por termo ou a partir de arquivos com URLs.

Arvore de arquivos do projeto:

```bash
video-dataset-creator/
├── crawlers/
│     ├── __init__.py
│     ├── rnp/
│     │     ├── __init__.py
│     │     ├── README.md
│     │     └── rnp_crawler.py
│     ├── tests/
│     │     ├── __init__.py
│     │     ├── test_rnp_crawler.py
│     │     ├── test_urls.csv
│     │     ├── test_yt_downloader_from_csv.py
│     │     ├── test_yt_search.py
│     │     ├── utils.py
│     │     └── xml_sample.pickle
│     └── youtube/
│           ├── __init__.py
│           ├── README.md
│           ├── yt_downloader_from_csv.py
│           └── yt_search.py
├── docs/
│     ├── _build/
│     │     ├── doctrees/
│     │     │     └── ...
│     │     ├── html/
│     │     │     └── ...
│     │     └── latex/
│     │           └── ...
│     ├── conf.py
│     ├── crawlers.rnp.rst
│     ├── crawlers.rst
│     ├── crawlers.youtube.rst
│     ├── index.rst
│     ├── make.bat
│     ├── Makefile
│     ├── modules.rst
│     ├── _static
│     └── _templates
├── __init__.py
├── LICENSE
├── Pipfile
├── Pipfile.lock
└── README.md
```

Documentação para o Usuário
===========================

Essas orientações para instalação serão majoritariamente focadas em um
usuário utilizando uma distribuição Linux como sistema operacional, dado
que a grande parte dos servidores, onde se é visada a execução dessas
ferramentas, utilizam distribuições Linux como sistema operacional. Não
obstante, essas ferramentas ainda podem ser utilizadas em qualquer
sistema operacional que suporte a execução de scripts *Python*.
Primeiro, o usuário deve fazer o download do projeto, que pode ser feito
pelo site GitHub.[^1]. Este pode ser feito como .zip diretamente pelo
site ou através do comando:

        $ git clone https://github.com/pedropva/video-dataset-creator.git    

Em seguida, é necessário verificar a existência de uma versão *Python*
compatível (A sua versão *Python* precisa ser 3.6.12 ou mais recente):

        $ python --version
        Python 3.6.12

Caso não tenha uma versão *Python* mais recente que 3.6.12, o usuário
pode usar o pacote *pyenv*[^2] para instalar a versão *Python* desejada,
sem interferir com a versão Python do sistema.

Para fazer a instalação das ferramentas e das suas dependências basta
usar o comando *Pipenv*[^3].

        $ pipenv install

Você também pode especificar o caminho para uma versão do python com
*--python*.

        $ pipenv install --python ~/.pyenv/versions/3.6.12/bin/python

Uma vez instalados o ambiente e dependências, basta utilizar o comando
*pipenv run* para executar as ferramentas. Também é possível criar uma
instancia de um terminal com esse ambiente com *pipenv run*, todos os
comandos *Python* executados dentro desse terminal implicação no uso do
interpretador *Python* selecionado, juntamente com as dependencias
instaladas.

Executando as ferramentas para coleta no Youtube
------------------------------------------------

Para executar a ferramenta para busca e coleta de vídeos, basta usar o
seguinte comando enquanto dentro de um terminal pipenv (*pipenv shell*)
ou utilizando o prefixo *pipenv run*:

         $ python yt_search.py Dança ~/ --number 5 --wait 5

Com esse comando a ferramenta buscará pela palavra “Dança” e coletará 5
vídeos, com intervalo de tempo entre 5 segundos entre as requisições
para download. Esse tempo de espera entre os downloads serve com um meio
de evitar que o algoritmo ultrapasse o limite de requisições por minuto
do Youtube, o que causaria um bloqueio temporário das requisições e
impossibilitaria o download continuo de vídeos. A ferramenta também
criará uma pasta chamada *Dança\_videos/* na pasta *home* do usuário
(Pois a pasta de destino especificada foi “ /”) e lá armazenará os
vídeos baixados.

Há uma opção para ajuda, caso o usuário tenha alguma dúvida sobre quais
argumentos usar, como mostra a Figura seguinte

![Página de ajuda da ferramenta Youtube
Search.](img/yt_search_help.png "fig:")

Em casos de termos de busca compostos por mais de uma palavra é
necessário que o usuário utilize aspas duplas para demarcar o termo. Em
termos de busca simples (com apenas uma palavra), as aspas não são
necessárias. A Figura seguinte mostra um exemplo de
execução da ferramenta, buscando por um termo de busca composto (“Sphinx
cat”).

![Exemplo de execução da ferramenta para busca e coleta de videos no
Youtube.](img/download_yt_search.png "fig:") 

O uso da ferramenta *Youtube Downloader from CSV* é similar, basta usar
o seguinte comando enquanto dentro de um terminal pipenv (*pipenv
shell*) ou utilizando o prefixo *pipenv run*:

         $ python yt_downloader_from_csv.py ../tests/test_urls.csv ~/yt_csv_downloads/

Com esse comando a ferramenta irá baixar todos os vídeos no arquivo
*test\_urls.csv*, que vem com as ferramentas, como parte do módulo de
testes. Além disso, se a pasta *yt\_csv\_downloads/* ainda não existir
na pasta *home* do usuário, a ferramenta a criará e salvará os vídeos
coletados nela.

Há uma opção para ajuda e consulta, como mostra a Figura
seguinte

![Página de ajuda da ferramenta Youtube Downloader from
CSV.](img/yt_downloader_from_csv_help.png "fig:")

A ferramenta também tentará fazer download de quaisquer vídeos na lista
que ainda não tenham sido baixados, como mostra a Figura seguinte:

![Exemplo de execução da ferramenta para coleta de vídeos no Youtube a
partir de um arquivo
CSV.](img/download_missing_yt_downloader_from_csv.png "fig:")

Executando a ferramenta para coleta na plataforma Video@RNP {#sec:user_rnp}
-----------------------------------------------------------

Para executar a ferramenta para coleta de vídeos através da API da
plataforma Video@RNP é necessário que o usuário primero tenha uma chave.
Para obter uma chave é necessário entrar em contato através da página de
contato do
[site](http://www.videoaula.rnp.br/portal/contact-render.action).[^4]

Uma vez de posse da chave de cliente para acesso à API, basta usar o
seguinte comando enquanto dentro de um terminal pipenv (*pipenv shell*)
ou utilizando o prefixo *pipenv run*:

         $  python rnp_crawler.py ~/rnp_videos/ --key \$CLIENT_KEY --limit 3

Com esse comando a ferramenta coletará 3 vídeos, com intervalo de tempo
entre 50 segundos entre as requisições para download (Tal tempo é
imposto pela plataforma). Esse tempo de espera entre os downloads serve
com um meio de evitar que o algoritmo ultrapasse o limite de requisições
por minuto da plataforma, o que causaria um bloqueio temporário das
requisições e impossibilitaria o download continuo de vídeos. A
ferramenta também criará uma pasta chamada *rnp\_videos/* (Caso não
exista) no diretório *home* do usuário e lá armazenará os vídeos
baixados.

Os seguintes argumentos podem usados para ajustar fatores como por qual
vídeo começar a coleta, se e onde salvar a saída e a quantidade de
vídeos baixados:

-   **key** (obrigatório): É a chave de acesso à API. Deve ser fornecida
    pelo suporte da plataforma.

-   **save\_dir** (obrigatório): O caminho para a pasta onde salvar os
    videos coletados, se não existir a ferramenta criará a pasta nesse
    caminho.

-   **limit** (opcional): Define o número de vídeos a se coletar.

-   **start\_id** (opcional): Define o id do vídeo pelo qual começar,
    caso o usário deseje vídeos específicos.

-   **start\_index** (opcional): Define de que pronto começar a coleta,
    para casos onde a ferramenta parou e precisa iniciar de certo ponto.

-   **log\_path** (opcional): Se fornecido, a ferramenta criará um
    arquivo chamado “probing.log” onde escreverá a saída padrão e outros
    dados de sua execução.

Há uma opção para ajuda e consulta de argumentos, como mostra a Figura
seguinte:

![Página de ajuda da ferramenta RNP
Crawler.](img/rnp_crawler_help.png "fig:")

A ferramenta foi feita com a intenção de baixar todos os vídeos da
plataforma. Ela também evita automaticamente coletar vídeos que já foram
baixados. A Figura seguinte mostra um exemplo de execução da
ferramenta, coletando 3 vídeos, sendo que dois deles já estavam
baixados.

![Exemplo de execução da ferramenta para coleta de vídeos da plataforma
Video@RNP.](img/download_missing_rnp_crawler.png "fig:")

[^1]: https://github.com/pedropva/video-dataset-creator

[^2]: https://github.com/pyenv/pyenv

[^3]: https://pypi.org/project/pipenv/

[^4]: http://www.videoaula.rnp.br/portal/contact-render.action

