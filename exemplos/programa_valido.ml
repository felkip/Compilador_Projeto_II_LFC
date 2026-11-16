// Programa válido da MiniLang: usa atribuição, aritmética com
// precedência, while, for, if/else, print e comentários.
x = 10;
y = 2 * (x + 5);      // 2 * 15 = 30
print(y);

/* contagem regressiva com while */
while (x > 0) {
  print(x);
  x = x - 1;
}

soma = 0;
for (i = 0; i < 5; i = i + 1) {
  soma = soma + i;    // 0 + 1 + 2 + 3 + 4 = 10
}

if (soma > 20) {
  print(soma);
} else {
  print(0);
}

// booleanos e comparação de igualdade
terminou = x == 0;
print(terminou);      // true
print(-7 / 2);        // divisão inteira truncada: -3
