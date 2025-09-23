from bs4 import BeautifulSoup
import requests
from unidecode import unidecode
import re
import time
import random

def get_url(singer, song):
    base_url = "https://www.vagalume.com.br/"

    singer = unidecode(singer.lower().replace(" ", "-"))
    song = unidecode(song.lower().replace(" ", "-") + '.html')

    return f"{base_url}{singer}/{song}"

def get_song_html(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erro ao buscar URL: {e}")
        return None

    soup = BeautifulSoup(response.content, "html.parser")

    lyrics_div = soup.find("div", {"id": "lyrics"})
    return lyrics_div.get_text(separator="\n", strip=True) if lyrics_div else None

def normalize_song(song):
    song = unidecode(song.lower())
    song = re.sub(r"[^\w\s]", " ", song)
    song = re.sub(r"[ \t]+", " ", song)
    song = re.sub(r"\n\s*", "\n", song).strip()
    return song

# lista expandida de artistas e musicas
singers_songs = {
    "Titãs": ["Epitáfio", "Enquanto Houver Sol", "Flores", "Marvin", "Polícia"],
    "Legião Urbana": ["Tempo Perdido", "Será", "Pais e Filhos", "Que País É Este", "Faroeste Caboclo"],
    "Os Paralamas do Sucesso": ["Alagados", "Lanterna dos Afogados", "Uma Brasileira", "Caleidoscópio"],
    "Capital Inicial": ["Primeiros Erros", "Natasha", "Fogo", "À Sua Maneira"],
    "Cazuza": ["Exagerado", "Brasil", "O Tempo Não Para", "Ideologia"],
    "Engenheiros do Hawaii": ["Terra de Gigantes", "Infinita Highway", "Pra Ser Sincero", "Era Um Garoto"],
    "Raul Seixas": ["Maluco Beleza", "Ouro de Tolo", "Metamorfose Ambulante", "Tente Outra Vez"],
    "Secos & Molhados": ["Sangue Latino", "Rosa de Hiroshima", "O Vira"],
    "RPM": ["Louras Geladas", "Rádio Pirata", "Alvorada Voraz"],
    "Barão Vermelho": ["Bete Balanço", "Por Que a Gente É Assim?", "Pense e Dance"],
    "Skank": ["Resposta", "Garota Nacional", "Acima do Sol", "Saideira"],
    "Jota Quest": ["Fácil", "As Dores do Mundo", "Onibus", "Do Seu Lado"],
    "Charlie Brown Jr.": ["Zóio de Lula", "Proibida pra Mim", "Tudo Que Ela Gosta de Escutar"],
    "Ivete Sangalo": ["Festa", "Acelerou", "Berimbau Metalizado"],
    "Chico Buarque": ["Construção", "Apesar de Você", "Cálice", "Roda Viva"],
    "Caetano Veloso": ["Sozinho", "Tropicália", "Você é Linda"],
    "Gilberto Gil": ["Toda Menina Baiana", "Refazenda", "Palco"],
    "Maria Bethânia": ["Carcará", "Reconvexo", "Olhos nos Olhos"],
    "Elis Regina": ["Como Nossos Pais", "Águas de Março", "O Que Foi Feito Deverá"],
    "Adoniran Barbosa": ["Trem das Onze", "Samba do Arnesto", "Iracema"],
    "Cartola": ["Preciso Me Encontrar", "O Mundo É Um Moinho", "Alvorada"],
    "Noel Rosa": ["Com Que Roupa?", "Feitiço da Vila", "Conversa de Botequim"],
    "Tom Jobim": ["Garota de Ipanema", "Chega de Saudade", "Insensatez"],
    "Vinícius de Moraes": ["Carta ao Tom", "Tarde em Itapuã", "A Casa"],
    "Toquinho": ["Aquarela", "Tarde em Itapuã", "Regra Três"],
    "Tim Maia": ["Gostava Tanto de Você", "Não Quero Dinheiro", "Descobridor dos Sete Mares"],
    "Jorge Ben Jor": ["Mas Que Nada", "País Tropical", "Fio Maravilha"],
    "Roberto Carlos": ["Detalhes", "Emoções", "O Calhambeque"],
    "Erasmo Carlos": ["Sentado à Beira do Caminho", "Mulher", "Festa de Arromba"],
    "Rita Lee": ["Mania de Você", "Lança Perfume", "Ovelha Negra"],
    "Mutantes": ["Panis et Circenses", "Ando Meio Desligado", "Balada do Louco"],
    "Novos Baianos": ["Brasil Pandeiro", "Preta Pretinha", "Bestinha"],
    "Belchior": ["Como Nossos Pais", "A Palo Seco", "Velha Roupa Colorida"],
    "Alceu Valença": ["La Belle de Jour", "Anunciação", "Tropicana"],
    "Fagner": ["Borbulhas de Amor", "Canteiros", "Deslizes"],
    "Zé Ramalho": ["Admirável Gado Novo", "Avôhai", "Frevo Mulher"],
    "Gonzaguinha": ["O Que É O Que É", "Lindo Lago do Amor", "Começaria Tudo Outra Vez"],
    "Ney Matogrosso": ["Homem com H", "Bandoleiro", "Pescador de Ilusões"],
    "Kid Abelha": ["Como Eu Quero", "Fixação", "Grande Hotel"],
    "Pato Fu": ["Ando Meio Desligado", "Música de Amor", "Antes que Seja Tarde"],
    "Os Mutantes": ["Panis et Circenses", "Ando Meio Desligado", "Balada do Louco"],
    "Los Hermanos": ["Anna Júlia", "O Vento", "Todo Carnaval Tem Seu Fim"],
    "Cássia Eller": ["Malandragem", "O Segundo Sol", "Relampiano"],
    "Marisa Monte": ["Bem Que Se Quis", "Depois", "Amor I Love You"],
    "Tribalistas": ["Já Sei Namorar", "Velha Infância", "É Você"],
    "O Rappa": ["Minha Alma", "Pescador de Ilusões", "Reza Vela"],
    "Nação Zumbi": ["Maracatu Atômico", "Da Lama Ao Caos", "A Cidade"],
    "Planet Hemp": ["Adoled", "Legalize Já", "Mantenha o Respeito"],
    "Racionais MC's": ["Diário de Um Detento", "Vida Loka", "Negro Drama"],
    "Sabotage": ["Respeito é Pra Quem Tem", "Rap é Compromisso", "Um Bom Lugar"],
    "Emicida": ["Triunfo", "Mandume", "Sujeito de Sorte"],
    "Criolo": ["Não Existe Amor em SP", "Lion Man", "Bogotá"]
}

# cria um checkpoint, caso precise interromper e continuar depois
def save_with_checkpoint(singers_songs, filename="corpus.txt", checkpoint_file="checkpoint.txt"):
    try:
        with open(checkpoint_file, "r") as f:
            last_artist = f.readline().strip()
            last_song = f.readline().strip()
            checkpoint_found = True
    except FileNotFoundError:
        checkpoint_found = False
    
    with open(filename, "a", encoding="utf-8") as f:
        artist_started = not checkpoint_found
        
        for singer, songs in singers_songs.items():
            if checkpoint_found and not artist_started:
                if singer == last_artist:
                    artist_started = True
                    song_started = False
                else:
                    continue
            
            for song in songs:
                if checkpoint_found and artist_started and not song_started:
                    if song == last_song:
                        song_started = True
                    continue
                
                print(f"Baixando {song} de {singer}...")
                url = get_url(singer, song)
                song_lyrics = get_song_html(url)
                
                if song_lyrics:
                    normalized = normalize_song(song_lyrics)
                    # f.write(f"{singer} - {song}\n")
                    f.write(f"{normalized}\n\n")
                    f.flush()  # força escrita imediata
                    
                    # Salvar checkpoint
                    with open(checkpoint_file, "w") as checkpoint:
                        checkpoint.write(f"{singer}\n")
                        checkpoint.write(f"{song}\n")
                
                # delay aleatorio para nao sobrecarregar o servidor
                time.sleep(random.uniform(1, 3))
        
        # remove o checkpoint apos a conclusao
        try:
            import os
            os.remove(checkpoint_file)
        except:
            pass


print("Iniciando coleta de letras musicais...")
save_with_checkpoint(singers_songs)
print("Coleta concluída! Corpus salvo em 'corpus.txt'")