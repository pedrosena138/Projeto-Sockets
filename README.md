# Projeto-Sockets
Chat P2P em python

- Qualquer peer poderá criar uma sala. O peer criador da sala é chamado de admin.
    - Após criada a sala outros peers poderão pedir para entrar na sala.
    - Todas as mensagens enviadas na sala deverá ser enviada para todos os integrantes da sala.
- Caso o admin fique offline outro peer deverá assumir o papel de admin
- O admin pode expulsar pessoas da sala, e bani-las de entrar na sala.
- Caso dois peers estejam na mesma sala, eles podem mandar uma mensagem privada entre eles. Essa mensagem não pode passar por nenhum outro peer.
- Caso um peer saia da sala, o atual admin deverá avisar a sala inteira que aquele peer caiu, mandando uma mensagem "Peer {id} saiu da sala"
