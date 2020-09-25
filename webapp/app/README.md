
# Regulação automática de encaminhamentos

## Apresentação

Neste componente de software está encapsulado um classificador automático de textos
que usa uma rede neural para classificar encaminhamentos a partir da descrição do <i>Quadro Clínico</i>.


## Como utilizar

O endereço de *endpoint* para utilizar o classificador é `/regulate` um parâmtro **t** pode ser adicionado na URL da requisição para determinar o *Threshould* acima do qual os exemplos serão classificados na classe positiva. Por exemplo, submter os dados de classificação à URL `/regulate?t=0.3` fará com que qualquer caso cuja probabilidade de pertencer à classe positiva for **maior que 0.3** seja associado a esta classe.

Há duas formas de invocar este endpoint. Enviando os dados diretamente, como [JSON](https://www.json.org/json-pt.html), ou enviando uma planilha excel. Seguem os detalhes.

### Enviando os dados como JSON

Para utilizar este método deve ser feita uma requisição HTTP POST, para o endereço 
`/regulate`

O corpo da requisição deverá conter um atributo **solicitacoes** com lista dos textos de quadro clínico de cada caso a ser regulado. Por exemplo:

```
{
    "solicitacoes": [
        "Paciente com relatos de hiperplasia prostática benigna desde 2010, pelo qual já realizou tratamento ( não bem definido ) com doxazosina 2 mg + finasterida 5 mg 1 cp a noite, agora refere estar tomando apenas doxazosina, assintomático no momento. Teve acompanhamento com urologista até março 2018. Solicita encaminhamento ao especialista pelo SUS. \nExames 14/02/18: PSAL 0,35 / PSAT 2,20 / creatinina 0,8.",
        "A paciente com cálculo no setor médio e cálice do polo inferior do rim direito, com 9mm e 33mm, com características que sugerem cálculo coraliforme, com discreta dilatação de alguns cálices, sintomática, necessitando de consulta e avaliação."
    ]
}
```


A resposta retornada será também um objeto JSON contendo dois atributos. Um deles, nomeado *pred_bins*,  conterá uma lista com valores 0 ou 1 representando, respectivamente, a Não-autorização ou a Autorização do caso. O outro, nomeado *pred_probas*, conterá uma lista de listas, em que cada uma das sublistas contém dois valores que representam, respectivamente, a probabilidade do caso ser considerado Não-aprovado e a probabilidade do ser considerado Aprovado. O exemplo de saída para as entradas acima seria:

```json
{
  "pred_bin": {
    "0": 0,
    "1": 1
  },
  "pred_probas": {
    "0": [
      0.6014226973,
      0.3985773027
    ],
    "1": [
      0.0897192359,
      0.9102807641
    ]
  }
}
```

#### Exemplo
Um exemplo de como realizar essas requisições pode ser visto no arquivo [cli/json.html](cli/json.html), neste repositório.

### Enviando uma Planila xlsx


Para utilizar este método deve ser feita uma requisição HTTP POST para o endereço  `/regulate`. A requisição deve conter um arquivo em um campo nomeado como **"spreadsheet"**. O arquivo deve ser uma planilha contendo uma coluna intitulada <strong>QUADROCLINICO</strong>. 

Cada linha da planilha deve corresponder a um caso a ser regulado e a coluna QUADROCLINICO deve conter o texto do quadro clínico do caso. As demais colunas que eventualmente existam serão ignoradas para fins de classificação.

O retorno será uma cópia da mesma planilha com as seguintes três novas colunas:

* _APROVADO: Conterá 0 (Não-Aprovado) ou 1 (Aprovado)
* _PROBA_0: Probabilidade do caso pertencer à classe Não-Aprovado
* _PROBA_1: Probabilidade do caso pertencer à classe Aprovado

#### Exemplo
Um exemplo de como realizar essas requisições pode ser visto no arquivo [cli/form.html](cli/form.html) deste repositório.