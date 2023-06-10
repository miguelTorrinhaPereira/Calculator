from math import *

class pilha:

    def __init__(self):self.p = []

    def empurra(self,elemento):self.p += [elemento]

    def tira(self):return self.p.pop()

    def ultimo(self):return self.p[-1]

    def vazia(self):return self.p == []



def rounds_aux(n,carry):
    if carry:
        if len(n) == 1:
            if n == '9': return '10'
            else: return str(int(n) + 1)
        else:
            if n[-2] == '9' and int(n[-1]) > 4:return rounds_aux(n[:-1],True) + '0'
            else: return n[:-2] + str(int(n[-2]) + 1)
    else:
      if n[-2] == '9' and int(n[-1]) > 4:return rounds_aux(n[:-1],True)
      elif len(n) == 2:return str(int(n[0]) + (int(n[1]) > 4))
      else:return n[:-2] + str(int(n[-2]) + (int(n[-1]) > 4))


def rounds(n):
    if '.' in n:
        pos_ponto = n.index('.')
        n = n.replace('.', '')
        t_inicial = len(n)
        n = rounds_aux(n,False)
        if len(n) > pos_ponto + (len(n) == t_inicial):
            if len(n)==t_inicial:pos_ponto = -len(n)+pos_ponto+1
            return n[:pos_ponto] + '.' + n[pos_ponto:]
        else:return n
    else:return rounds_aux(n,False)


def alg_sig(n):
    n =  n.replace('-','')
    if 'e' in n:return len(n.split('e')[0]) - ('.' in n)
    else:
        n = n.replace('.', '')
        for i in range(len(n)):
            if n[i] != '0': return len(n) - i


def alg_dec(n):
    if 'e' in n:
        m,e = n.split('e')
        algs =  len(m) - 2 - int(e)
    else:
        if '.' in n:algs =  len(n.split('.')[-1])
        else:return  0
    return max(algs,0)

def correct_algs_sig(n,algs,algs_atual):
    if algs_atual == algs:pass
    elif algs_atual < algs:n = n + '.'*('.'not in n) + '0' * (algs - algs_atual)
    else:
        if '.' not in n or len(n)-(algs_atual - algs)-1 < n.index('.'):
            expi = calc_exp(n)
            n = n.replace('.','')
            n = n[:len(n) - (algs_atual-algs)+1]
            size_i = len(n)
            n = rounds(n)
            if size_i == len(n):n,expi = n[:-1], expi + 1
            n = exp_form(n)
            if 'e' not in n:return n + 'e' + str(expi) if expi != 0 else n
            else: return n.split('e')[0] + 'e' + str(expi)
        else:
            n = n[:len(n) - (algs_atual - algs - 1)]
            n = rounds(n)
            if alg_sig(n)==algs+1:return correct_algs_sig(n,algs,algs+1)
    return exp_form(n)


def correct_algs_dec(n,algs,algs_atual):
    if algs_atual == algs:pass
    elif algs_atual < algs:n = n + '.'*('.'not in n) + '0' * (algs - algs_atual)
    else:
        n = n[:len(n)-(algs_atual-algs)+1]
        n = rounds(n)
    return n


def calc_exp(n): return floor(log10(abs(eval(n))))


def exp_form(n):
  exp = calc_exp(n)
  if exp == 0: exp = ''
  else:exp = 'e' + str(exp)

  mant = ''
  n = n.replace('.', '')
  for i in range(len(n)):
    if n[i] != '0':
      mant = mant + n[i:]
      break
  mant = mant.replace('-', '')
  if len(mant) == 1:mant = str(mant)
  else:mant = mant[0] + '.' + mant[1:]
  if '-' in n and '-' not in mant: mant = '-' + mant

  return mant + exp


def mult(n1, n2):
    n = str(eval('{}*{}'.format(n1, n2)))
    algs = min(alg_sig(n1), alg_sig(n2))
    algs_atual = alg_sig(n)
    return correct_algs_sig(n,algs,algs_atual)


def exp(n1, n2):
    n = str(eval('{}**{}'.format(n1, n2)))
    algs = alg_sig(n1)
    algs_atual = alg_sig(n)
    return correct_algs_sig(n,algs,algs_atual)


def div(n1, n2):
    n = str(eval('{}/{}'.format(n1, n2)))
    algs = min(alg_sig(n1), alg_sig(n2))
    algs_atual = alg_sig(n)
    return correct_algs_sig(n,algs,algs_atual)


def add(n1,n2):
    n=str(eval('{}+{}'.format(n1,n2)))
    algs = min(alg_dec(n1), alg_dec(n2))
    algs_atual = alg_dec(n)
    return correct_algs_dec(n,algs,algs_atual)


def sub(n1, n2):
    n = str(eval('{}-{}'.format(n1, n2)))
    algs = min(alg_dec(n1), alg_dec(n2))
    algs_atual = alg_dec(n)
    return correct_algs_dec(n,algs,algs_atual)


def calcula_aux(operacoes,i,operacao):
    operacoes[i] = operacao(operacoes[i-1],operacoes[i+1])
    del(operacoes[i+1])
    del(operacoes[i-1])


def calcula(operacoes):
    i = 0
    while i < len(operacoes):
        if operacoes[i] == '**':calcula_aux(operacoes,i,exp)
        else:i += 1
    i = 0
    while i < len(operacoes):
        if operacoes[i] == '*':calcula_aux(operacoes,i,mult)
        elif operacoes[i] == '/':calcula_aux(operacoes,i,div)
        else: i += 1
    i = 0
    while i < len(operacoes):
        if operacoes[i] == '+':calcula_aux(operacoes,i,add)
        elif operacoes[i] == '-':calcula_aux(operacoes,i,sub)
        else: i += 1
    return operacoes[0]


def identifica_numero(calc,i):
    numero = calc[i]
    while True:
        i += 1
        digit = calc[i]
        if digit.isdigit() or digit == 'e' or digit == '.' or digit == '-':numero += digit
        else:return numero,i


def identifica_parenteces(calc,i):
    opostos = {'(':')','[':']'}
    p = pilha()
    p.empurra(calc[i])
    calc_p = ''
    while True:
        i += 1
        c = calc[i]
        if c == '(' or c == '[':p.empurra(c)
        elif c == opostos[p.ultimo()]:p.tira()
        if p.vazia():return calc_p,i
        calc_p += c


def tratamento(calc):
    dict_translate = {247:'/',215:'*',8722:'-'}

    calc = calc.translate(dict_translate)
    calc = calc.replace('√','sqrt')
    calc = calc.replace('ln','log')
    calc = calc.replace('fact','factorial')

    calc = calc + ' '
    operadores = ['+','-','*','/']
    operacoes = []
    i = 0
    while i < len(calc):
        c = calc[i]
        if c == '^':
            operacoes += ['**']
            i += 1
        elif c in operadores:
            operacoes += c
            i += 1
        elif c.isdigit():
            info = identifica_numero(calc,i)
            operacoes += [info[0]]
            i = info[1]
        elif c.isalpha():
            func = ''
            while calc[i]!='[':
                func += calc[i]
                i+=1
            info = identifica_parenteces(calc,i)
            arg = processar(info[0])
            algs = alg_sig(info[0])
            n = str(eval(func+'('+arg+')' ))
            algs_atual = alg_sig(n)
            operacoes += [correct_algs_sig(n,algs,algs_atual)]
            i = info[1]
        elif c=='(':
            info = identifica_parenteces(calc,i)
            calc = calc[:i] + info[0] + calc[info[1]+1:]
        else:
            i += 1
    return operacoes


def processar(calc):
    return calcula(tratamento(calc))