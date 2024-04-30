import pygame
import random
import csv

pygame.init()

# Cores
cores = {'branco': (255, 255, 255), 'preto': (0, 0, 0), 'verde': (0, 255, 0), 'cinza': (128, 128, 128), 'vermelho': (255, 0, 0)}

def posicionar_comida(largura, altura, tamanho_bloco, cobra_lista):
    comida_tamanho = tamanho_bloco // 2

    # Área jogável dentro dos limites das paredes
    area_jogavel_x1 = tamanho_bloco
    area_jogavel_y1 = tamanho_bloco
    area_jogavel_x2 = largura - tamanho_bloco
    area_jogavel_y2 = altura - tamanho_bloco

    # Lista de todas as grades possíveis na área jogável
    grades_disponiveis = []

    for x in range(area_jogavel_x1 // tamanho_bloco, area_jogavel_x2 // tamanho_bloco):
        for y in range(area_jogavel_y1 // tamanho_bloco, area_jogavel_y2 // tamanho_bloco):
            if [x * tamanho_bloco, y * tamanho_bloco] not in cobra_lista:
                grades_disponiveis.append((x, y))

    if grades_disponiveis:
        # Determinar se a comida especial será ativada (1 em 10)
        comida_especial_ativa = random.randint(1, 10) == 1

        if comida_especial_ativa:
            # Escolher aleatoriamente uma grade disponível para a comida especial
            comida_especial_grade = random.choice(grades_disponiveis)
            comida_especial_x = comida_especial_grade[0] * tamanho_bloco + (tamanho_bloco - comida_tamanho) // 2
            comida_especial_y = comida_especial_grade[1] * tamanho_bloco + (tamanho_bloco - comida_tamanho) // 2
        else:
            # A comida especial não está ativa
            comida_especial_x, comida_especial_y = -1, -1

        # Escolher aleatoriamente uma grade disponível para a comida normal
        comida_grade = random.choice(grades_disponiveis)
        comida_x = comida_grade[0] * tamanho_bloco + (tamanho_bloco - comida_tamanho) // 2
        comida_y = comida_grade[1] * tamanho_bloco + (tamanho_bloco - comida_tamanho) // 2
    else:
        # Se não houver grades disponíveis para o jogo.
        comida_x, comida_y = -1, -1
        comida_especial_ativa = False
        comida_especial_x, comida_especial_y = -1, -1

    return comida_x, comida_y, comida_especial_ativa, comida_especial_x, comida_especial_y

def mostrar_novo_recorde(tela, largura, altura, pontuacao):
    font_size = min(largura // 22, altura // 18)
    fonte = pygame.font.SysFont('comicsansms', font_size)
    texto_novo_recorde = "Novo Recorde!"
    texto_pontuacao = f"Pontuação: {pontuacao}"
    texto_iniciais = "Insira suas iniciais (3 letras):"

    input_texto = ""

    while len(input_texto) != 3:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.unicode.isalpha() and len(input_texto) < 3:
                    input_texto += event.unicode.upper()
                elif event.key == pygame.K_RETURN and len(input_texto) == 3:
                    return input_texto  # Retorna as iniciais quando o Enter for pressionado

        tela.fill(cores['branco'])

        # Renderizar texto na tela
        texto_render = fonte.render(texto_novo_recorde, True, cores['preto'])
        pos_x = (largura - texto_render.get_width()) // 2
        pos_y = altura // 4
        tela.blit(texto_render, (pos_x, pos_y))

        texto_render = fonte.render(texto_pontuacao, True, cores['preto'])
        pos_y += font_size + 10
        tela.blit(texto_render, (pos_x, pos_y))

        texto_render = fonte.render(texto_iniciais, True, cores['preto'])
        pos_y += font_size + 20
        tela.blit(texto_render, (pos_x, pos_y))

        texto_digitado_render = fonte.render(input_texto, True, cores['preto'])
        pos_y += font_size + 10
        tela.blit(texto_digitado_render, (pos_x, pos_y))

        pygame.display.update()

    return input_texto

def mostrar_ranking(tela, largura, altura, ranking):
    font_size = min(largura // 18, altura // 18)
    fonte = pygame.font.SysFont('comicsansms', font_size)
    font_size_ranking = font_size // 2
    fonte_ranking = pygame.font.SysFont('comicsansms', font_size_ranking)

    tela.fill(cores['branco'])

    texto_ranking = "Top Pontuações:"
    texto_render = fonte.render(texto_ranking, True, cores['preto'])
    pos_x = (largura - texto_render.get_width()) // 2
    pos_y = altura // 4
    tela.blit(texto_render, (pos_x, pos_y))

    pos_y += font_size + 10
    for i, registro in enumerate(ranking[:10], start=1):
        texto_registro = f"{i}. {registro['Jogador']} - {registro['Pontuacao']}"
        texto_render = fonte_ranking.render(texto_registro, True, cores['preto'])
        tela.blit(texto_render, (pos_x, pos_y))
        pos_y += font_size_ranking + 5

    texto_continuar = "Pressione ENTER para continuar"
    texto_render_continuar = fonte.render(texto_continuar, True, cores['preto'])
    pos_x = (largura - texto_render_continuar.get_width()) // 2
    pos_y = altura - font_size * 2
    tela.blit(texto_render_continuar, (pos_x, pos_y))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

def mostrar_game_over(tela, largura, altura, pontuacao):
    font_size = min(largura // 24, altura // 24)
    fonte = pygame.font.SysFont('comicsansms', font_size)
    texto_game_over = "Game Over!"
    texto_game_over_render = fonte.render(texto_game_over, True, cores['preto'])

    tela.fill(cores['branco'])
    pos_x = (largura - texto_game_over_render.get_width()) // 2
    pos_y = (altura - texto_game_over_render.get_height()) // 2
    tela.blit(texto_game_over_render, (pos_x, pos_y))

    # Exibir pontuação
    texto_pontuacao = f"Pontuação: {pontuacao}"
    texto_render = fonte.render(texto_pontuacao, True, cores['preto'])
    pos_y += font_size + 20
    tela.blit(texto_render, (pos_x, pos_y))

    # Exibir instruções para jogar novamente
    texto_instrucao = "Pressione ESPAÇO para jogar novamente"
    texto_instrucao2 = "Pressione ESC para sair"
    texto_render = fonte.render(texto_instrucao, True, cores['preto'])
    texto_render2 = fonte.render(texto_instrucao2, True, cores['preto'])

    pos_y += font_size * 2
    tela.blit(texto_render, ((largura - texto_render.get_width()) // 2, pos_y))
    pos_y += font_size + 10
    tela.blit(texto_render2, ((largura - texto_render2.get_width()) // 2, pos_y))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE:
                    return True

def adicionar_pontuacao(nome_jogador, pontuacao, ranking):
    # Converter pontuação para inteiro
    pontuacao = int(pontuacao)

    # Adicionar nova pontuação ao ranking
    ranking.append({'Jogador': nome_jogador, 'Pontuacao': pontuacao})

    # Converter todas as pontuações para inteiro antes de ordenar
    for registro in ranking:
        registro['Pontuacao'] = int(registro['Pontuacao'])

    # Ordenar o ranking por pontuação decrescente
    ranking.sort(key=lambda x: x['Pontuacao'], reverse=True)

    # Manter apenas as 10 melhores pontuações
    ranking = ranking[:10]

    return ranking

def salvar_ranking(ranking):
    # Salvar o ranking em um arquivo CSV
    with open('ranking.csv', 'w', newline='') as arquivo_csv:
        colunas = ['Jogador', 'Pontuacao']
        escritor_csv = csv.DictWriter(arquivo_csv, fieldnames=colunas)
        escritor_csv.writeheader()
        escritor_csv.writerows(ranking)

def carregar_ranking():
    try:
        # Carregar o ranking do arquivo CSV
        with open('ranking.csv', newline='') as arquivo_csv:
            leitor_csv = csv.DictReader(arquivo_csv)
            ranking = [dict(registro) for registro in leitor_csv]
    except FileNotFoundError:
        # Se o arquivo não existir, iniciar com ranking vazio
        ranking = []

    return ranking

def verificar_vitoria(largura, altura, tamanho_bloco, cobra_lista):
    # Determinar o número total de grades possíveis na área jogável
    grades_totais = ((largura - 2 * tamanho_bloco) // tamanho_bloco) * ((altura - 2 * tamanho_bloco) // tamanho_bloco)

    # Verificar se o comprimento da cobra cobre todas as grades disponíveis
    return len(cobra_lista) >= grades_totais

def mostrar_vitoria(tela, largura, altura):
    font_size = min(largura // 24, altura // 24)
    fonte = pygame.font.SysFont('comicsansms', font_size)
    texto_vitoria = "Parabéns! Você venceu!"
    texto_vitoria_render = fonte.render(texto_vitoria, True, cores['preto'])

    tela.fill(cores['branco'])
    pos_x = (largura - texto_vitoria_render.get_width()) // 2
    pos_y = (altura - texto_vitoria_render.get_height()) // 2
    tela.blit(texto_vitoria_render, (pos_x, pos_y))

    pygame.display.update()

def preencher_com_corpo(tela, largura, altura, tamanho_bloco, cobra_lista):
    for x in range(tamanho_bloco, largura - tamanho_bloco, tamanho_bloco):
        for y in range(tamanho_bloco, altura - tamanho_bloco, tamanho_bloco):
            if [x, y] not in cobra_lista:
                pygame.draw.rect(tela, cores['cinza'], [x, y, tamanho_bloco, tamanho_bloco])
    
    pygame.display.update()

def desenhar_limites(tela, largura, altura, tamanho_bloco):
    # Desenha linhas de limite ao redor da área de jogo
    linha_cor = cores['preto']
    pygame.draw.rect(tela, linha_cor, (0, 0, largura, tamanho_bloco))                      # Linha superior
    pygame.draw.rect(tela, linha_cor, (0, altura - tamanho_bloco, largura, tamanho_bloco))  # Linha inferior
    pygame.draw.rect(tela, linha_cor, (0, 0, tamanho_bloco, altura))                       # Linha esquerda
    pygame.draw.rect(tela, linha_cor, (largura - tamanho_bloco, 0, tamanho_bloco, altura))  # Linha direita

def jogo_snake():
    largura, altura = 400, 400
    tamanho_bloco = 20
    fps = 10

    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption('Snake Game')

    clock = pygame.time.Clock()

    # Cores da cobra
    cor_cobra_cabeca = 'cinza'
    cor_cobra_corpo = 'preto'

    while True:
        # Variáveis do jogo
        game_over = False
        movimento_inicial = True
        velocidade_x = 0
        velocidade_y = 0
        cobra_lista = []
        comprimento_cobra = 1
        posicao_x = largura // 2
        posicao_y = altura // 2
        ultima_direcao = None

        # Carregar ranking
        ranking = carregar_ranking()

        # Inicializar posição da comida
        (comida_x, comida_y, comida_especial_ativa, comida_especial_x, comida_especial_y) = posicionar_comida(largura, altura, tamanho_bloco, cobra_lista)

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return
                    elif event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                        if movimento_inicial:  # Permitir movimento apenas após o primeiro input
                            movimento_inicial = False
                        if (event.key == pygame.K_LEFT and ultima_direcao != pygame.K_RIGHT) or \
                           (event.key == pygame.K_RIGHT and ultima_direcao != pygame.K_LEFT) or \
                           (event.key == pygame.K_UP and ultima_direcao != pygame.K_DOWN) or \
                           (event.key == pygame.K_DOWN and ultima_direcao != pygame.K_UP):
                            ultima_direcao = event.key

            # Atualizar posição da cobra com base na última direção após primeiro input
            if not movimento_inicial:
                if ultima_direcao == pygame.K_LEFT and velocidade_x != tamanho_bloco:
                    velocidade_x = -tamanho_bloco
                    velocidade_y = 0
                elif ultima_direcao == pygame.K_RIGHT and velocidade_x != -tamanho_bloco:
                    velocidade_x = tamanho_bloco
                    velocidade_y = 0
                elif ultima_direcao == pygame.K_UP and velocidade_y != tamanho_bloco:
                    velocidade_x = 0
                    velocidade_y = -tamanho_bloco
                elif ultima_direcao == pygame.K_DOWN and velocidade_y != -tamanho_bloco:
                    velocidade_x = 0
                    velocidade_y = tamanho_bloco

            # Atualizar posição da cobra
            posicao_x += velocidade_x
            posicao_y += velocidade_y

            # Verificar colisões com bordas
            if posicao_x >= largura - tamanho_bloco or posicao_x < tamanho_bloco or \
               posicao_y >= altura - tamanho_bloco or posicao_y < tamanho_bloco:
                game_over = True

            # Verificar colisões consigo mesma
            if [posicao_x, posicao_y] in cobra_lista[:-1]:
                game_over = True

            # Atualizar lista da cobra
            cobra_cabeca = [posicao_x, posicao_y]
            cobra_lista.append(cobra_cabeca)

            if len(cobra_lista) > comprimento_cobra:
                del cobra_lista[0]

            # Desenhar elementos na tela
            tela.fill(cores['branco'])  # Preencher a tela com cor branca
            
            desenhar_limites(tela, largura, altura, tamanho_bloco)  # Desenhar linhas de limite

            # Verificar se a cobra comeu a comida
            if posicao_x <= comida_x < posicao_x + tamanho_bloco and posicao_y <= comida_y < posicao_y + tamanho_bloco:
                comprimento_cobra += 1
                # Atualizar posição da comida normal
                (comida_x, comida_y, comida_especial_ativa, comida_especial_x, comida_especial_y) = posicionar_comida(largura, altura, tamanho_bloco, cobra_lista)

                # Verificar se a comida especial deve aparecer
                if comida_especial_ativa and random.randint(1,10) == 1:
                    (comida_x, comida_y, _, comida_especial_x, comida_especial_y) = posicionar_comida(largura, altura, tamanho_bloco, cobra_lista)
           
            # Verificar se a cobra comeu a comida especial
            if comida_especial_ativa and posicao_x <= comida_especial_x < posicao_x + tamanho_bloco and posicao_y <= comida_especial_y < posicao_y + tamanho_bloco:
                comprimento_cobra += 2  # Aumentar o comprimento da cobra ao coletar comida especial
                comida_especial_ativa = False  # Desativar a comida especial

            # Desenhar a comida normal
            pygame.draw.rect(tela, cores['verde'], [comida_x, comida_y, tamanho_bloco // 2, tamanho_bloco // 2])

            # Desenhar a comida especial se estiver ativa
            if comida_especial_ativa:
                pygame.draw.rect(tela, cores['vermelho'], [comida_especial_x, comida_especial_y, tamanho_bloco // 2, tamanho_bloco // 2])

            # Desenhar a cabeça da cobra
            pygame.draw.rect(tela, cores[cor_cobra_cabeca], [posicao_x, posicao_y, tamanho_bloco, tamanho_bloco])

            # Desenhar o corpo da cobra
            for bloco in cobra_lista[:-1]:  # Desenhar o corpo da cobra excluindo a cabeça
                pygame.draw.rect(tela, cores[cor_cobra_corpo], [bloco[0], bloco[1], tamanho_bloco, tamanho_bloco])

            pygame.display.update()  # Atualizar a tela

            clock.tick(fps)

        # Calcular pontuação final
        pontuacao_final = (comprimento_cobra - 1) * 10

        # Verificar se a pontuação final é maior que a menor pontuação no top 10
        if len(ranking) < 10 or pontuacao_final > ranking[-1]['Pontuacao']:
            nome_jogador = mostrar_novo_recorde(tela, largura, altura, pontuacao_final)
            ranking = adicionar_pontuacao(nome_jogador, pontuacao_final, ranking)
            salvar_ranking(ranking)

        # Mostrar tela de game over e processar pontuação
        mostrar_ranking(tela, largura, altura, ranking)
        game_reiniciar = mostrar_game_over(tela, largura, altura, pontuacao_final)

        if not game_reiniciar:
            # Limpar variáveis da cobra e reiniciar a tela
            game_over = False
            movimento_inicial = True
            velocidade_x = 0
            velocidade_y = 0
            cobra_lista = []
            comprimento_cobra = 1
            posicao_x = largura // 2
            posicao_y = altura // 2
            ultima_direcao = None
            tela.fill(cores['branco'])

if __name__ == '__main__':
    jogo_snake()