## O que é

Essa é uma implementação do modelo de regulação automática de encaminhamentos produzido no trabalho de pesquisa intitulado
 **Desenvolvimento e Avaliação de Algoritmos de Classificação e Decisão na Regulação de Pacientes Encaminhados para a
Atenção Especializada Ambulatorial**.

O trabalho foi desenvolvido pelo aluno **Piter Oliveira Vergara**, do Programa de Pós-Graduação em Computação do Instituto de Informática da UFRGS, sob orientação do professor **Dr. Leandro Krug Wives**, em parceria com o **Dr. Dimitris Rucks Varvaki Rados**, do Programa de Pós-Graduação em Epidemiologia da Faculdade de Medicina da UFRGS, o **Dr. Rudi Roman**, do TelessaudeRS, e outros colaboradores.

Neste repositório encontra-se um componente de software que encapsula um classificador automático de textos
que usa uma rede neural para classificar encaminhamentos do TelessaúdeRS a partir da descrição do <i>Quadro Clínico</i>.

O modelo em si, bem como os embeddings utilizados na primeira camada da rede neural, não estão registrados neste repositório por questões de sigilo dos dados. Para utlizar efetivamente estes códigos será preciso obter uma cópia destes artefatos.

# Como utilizar

## Requisitos
Uma máquina com [Git](https://git-scm.com/), [Docker](https://docs.docker.com/) e [Docker compose](https://docs.docker.com/compose/)

## Passo-a-passo

* Clonar o repositório
* Obter cópia dos artefatos *model.hdf5* e *tokenizer.pkl.z* e substituir pelos que estão atualmete no repositório (são apenas *placeholders*)
* Construir a imagem dos containers
* Iniciar os container
* Acessar o serviço pela interface Web


## Exemplo

Abaixo, exemplos de como os passos acima podem ser realizados usando o console de um host que disponha dos pré-requisitos.


```bash
git clone git@github.com:pitervergara/telessauders-regulacao.git

cd telessauders-regulacao

# aqui, substituir o modelo e o tokenizer

docker-compose build 

docker-compose up -d
```


### Testes 

* Pelo navegador: Acessar o endereço da máquina na porta 8080 (ex.: http://localhost:8080)

* Também é possível testar diretamente o classificador, sem o componente web, executando o arquivo *classifier.py*
Ex.:
```bash
docker-compose run webapp python classifier.py
```

Nesse caso, o script do classificador irá ler os dois exemplos que estão no arquivo [app/data/test_dataset_out_etapa1.pkl.z](webapp/app/data/test_dataset_out_etapa1.pkl.z), classificá-los e imprimir o resultado. A saída esperada é:
```bash
Using TensorFlow backend.

{'pred_bin': [1, 0],
 'pred_probas': [[0.47743064165115356, 0.52256936],
                 [0.5889297425746918, 0.41107026]]}

 ```

 ## Mais detalhes

 Mais alguns detalhes sobre como usar este software constam no [README do aplicativo](webapp/app/README.md)

## Importante

Este container bem como a aplicação Web por ele exposta não foram desenvolvidos tendo em vista um ambiente real de produção. Trata-se apenas de uma Prova de Conceito de como o modelo de Aprendizado de Máquinas desenvolvido no trabalho de pesquisa pode ser utilizado para a classificação dos encaminhamimentos.