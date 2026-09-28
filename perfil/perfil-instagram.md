# Perfil de Instagram — @unattended.io

Los tres campos van desde la app o instagram.com. **Ninguno se puede cambiar por
API**: la Graph API de Instagram publica contenido, pero no toca el perfil.

---

## Foto de perfil

`avatar-instagram.png`, en esta misma carpeta. 1080 × 1080.

No es el logo completo: es la "u" y el caret a sangre sobre el negro de marca.
El logo oficial es un cuadrado redondeado, y el perfil de Instagram recorta en
círculo — se le cortarían las cuatro esquinas. Así llena el círculo y a 32 px en
el feed se sigue leyendo.

---

## Nombre  *(30 caracteres, y hoy está VACÍO)*

```
unattended · automatización IA
```

Es el arreglo más barato del perfil. Instagram indexa dos campos para búsqueda:
el usuario y el nombre. Con el nombre en blanco, la cuenta solo aparece si
alguien ya sabe cómo se llama — nadie llega buscando "automatización" o
"agentes de IA".

---

## Bio  *(150 caracteres)*

Es el eslogan de la página de LinkedIn, para que las dos redes digan lo mismo.
**145 de 150 caracteres** — quedan cinco, así que no le agregues nada sin volver
a contar.

```
Automatización que corre sola: agentes de IA a la medida
que ejecutan el trabajo repetitivo de tu empresa.
⚡ Leads · Soporte · Reportes · Captura
```

Si Instagram se queja de la longitud —a veces cuenta el emoji como más de un
carácter— quita la primera línea del listado y deja solo el eslogan: son 106
caracteres y sobra espacio.

**Qué cambia respecto a la bio de hoy.** La actual abre en inglés (*"We don't
build AI that talks"*) y sigue en español. La frase es buena, pero el público no
es ese: un dueño de hotel o de despacho en CDMX se topa con un cambio de idioma
en el primer renglón.

---

## Sitio web

```
https://unattended.io
```

Hoy está como `http://`, sin la ese. El sitio fuerza HTTPS, así que cada visita
desde la bio hace un redirect de más.

---

## Lo que ya quedó bien y no hay que tocar

- El usuario `@unattended.io` coincide con el dominio.
- La cuenta es tipo Empresa, que es lo que la API necesita para publicar.
