from Main import dificultad_por_ronda,siguiente_nivel,normalizar



def test_dificultad_por_ronda():
    assert dificultad_por_ronda(0) == "facil"
    assert dificultad_por_ronda(2) == "facil"
    assert dificultad_por_ronda(3) == "media"
    assert dificultad_por_ronda(5) == "media"
    assert dificultad_por_ronda(6) == "dificil"
    assert dificultad_por_ronda(99) == "dificil"

def test_siguiente_nivel():
    assert siguiente_nivel("facil") == "media"
    assert siguiente_nivel("media") == "dificil"
    assert siguiente_nivel("dificil") == "dificil"

def test_normalizar():
    assert normalizar("  Hola Mundo  ") == "hola mundo"
    assert normalizar("AdivinAr") == "adivinar"
    assert normalizar("  Programacion ") == "programacion"
