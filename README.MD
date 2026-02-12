# Controle de Combustível - Odoo 19

Módulo Odoo para controle de abastecimentos e estoque de combustível.

## Descrição

Sistema desenvolvido para gerenciar abastecimentos de veículos e controlar o estoque de combustível em tanques. Permite registrar abastecimentos, controlar entradas de combustível e gerenciar permissões por perfil de usuário.

## Como Utilizar Módulo
- Instalar os seguintes módulos: maintenance e controle_combustivel
- Depois de instalar os módulos, vá em: Definições > Usuários e Empresas > Grupos > procure por: Combustível > Irá aparecer os 3 grupos: Administrador, Analista, Motorista. > adicione seu usuário a um grupo > recarregue a pagina cntrl + f5 e o módulo irá aparecer.
- Primeiro você deve criar um tanque em: Estoque > Tanques, após criar tudo deverá funcionar normalmente.

## Vídeo Ensinando a Utilizar o Módulo:
- https://youtu.be/8nG5qFNMsuM

## Funcionalidades

### Abastecimentos
- Registro de abastecimentos vinculados a equipamentos/veículos
- Campos: data/hora, horímetro/odômetro, litros, valor por litro
- Cálculo automático do valor total
- Controle de motorista e responsável
- Validação de valores (não aceita negativos ou zero)
- Atualização automática do estoque ao confirmar

### Estoque de Combustível
- Gestão de tanques com capacidade definida (padrão: 6.000L)
- Entradas de combustível aumentam o estoque automaticamente
- Abastecimentos reduzem o estoque automaticamente
- Visualização do percentual de ocupação
- Validação de estoque insuficiente

### Permissões
- **Motorista**: Registra abastecimentos, visualiza estoque (sem alteração manual)
- **Analista**: Visualiza relatórios e dados
- **Administrador**: Acesso total ao sistema

## Requisitos

- Odoo 19 Community
- Módulo `maintenance` (dependência)