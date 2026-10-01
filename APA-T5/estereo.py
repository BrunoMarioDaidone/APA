"""
Bruno Mario Daidone Rossini

Documento que inclueye las funciones pedidas
(estereo2mono(), mono2estereo(), codEstereo(), decEstereo())
"""

import struct as st

def estereo2mono(ficEste, ficMono, canales=2):
"""
Función que transforma un fichero estereo en uno mono de distintas maneras
según se pida, siendo la opción por defecto la semisuma de los dos canales,
y las demás opciones todo en el canal L, todo en el canal R, y la semidiferencia
de los canales.
"""

    with open(ficEste, "rb") as file:
            formato = '<4sI4s'
            buffer = file.read(st.calcsize(formato))
            chunkId, chunkSize, chunkFormat=st.unpack(formato, buffer)

            formato = '<4sIHHIIHH'
            buffer = file.read(st.calcsize(formato))
            subChunk1Id, subChunk1Size, audioFormat, numChannels, sampleRate, byteRate, blockAlign, bitsPerSample=st.unpack(formato, buffer)
            if numChannels != 2:
                raise ValueError("El fichero debe ser estéreo")

            formato = '<4sI'
            buffer = file.read(st.calcsize(formato))
            subChunk2Id, subChunk2Size=st.unpack(formato, buffer)

            samplesNumber = int(subChunk2Size // (bitsPerSample // 8))

            formato = f"<{samplesNumber}h"
            buffer = file.read(st.calcsize(formato))
            samples=st.unpack(formato, buffer)

            left = samples[::2]
            right = samples[1::2]
                
            if canales == 0:
                mono = left
                
            elif canales == 1:
                mono = right

            elif canales == 2:
                mono = [(l + r) // 2 for l, r in zip(left, right)]

            else:
                mono = [(l - r) // 2 for l, r in zip(left, right)]

    with open(ficMono, "wb") as file:
        formato = '<4sI4s'
        datos = st.pack(formato, chunkId, chunkSize, chunkFormat)
        file.write(datos)
        
        formato = '<4sIHHIIHH'
        datos = st.pack(formato, subChunk1Id, subChunk1Size, audioFormat, 1, sampleRate, sampleRate * bitsPerSample // 8, bitsPerSample // 8, bitsPerSample)
        file.write(datos)
        
        formato = '<4sI'
        datos = st.pack(formato, subChunk2Id, len(mono) * bitsPerSample // 8)
        file.write(datos)
        
        formato = f"<{len(mono)}h"
        datos = st.pack(formato, *mono)
        file.write(datos)


def mono2estereo(ficIzq, ficDer, ficEste):
"""
Función que lee dos ficheros mono cada uno de un canal (L o R)
y con ellos escribe uno en estereo.
"""
    with open(ficIzq, "rb") as file:
        formato = '<4sI4s'
        buffer = file.read(st.calcsize(formato))
        chunkId, chunkSize, chunkFormat=st.unpack(formato, buffer)

        formato = '<4sIHHIIHH'
        buffer = file.read(st.calcsize(formato))
        subChunk1Id, subChunk1Size, audioFormat, numChannels, sampleRate, byteRate, blockAlign, bitsPerSample=st.unpack(formato, buffer)
        if numChannels != 1:
            raise ValueError("El fichero debe ser mono!")

        formato = '<4sI'
        buffer = file.read(st.calcsize(formato))
        subChunk2Id, subChunk2Size=st.unpack(formato, buffer)

        samplesNumber = int(subChunk2Size // (bitsPerSample // 8))

        formato = f"<{samplesNumber}h"
        buffer = file.read(st.calcsize(formato))
        samples=st.unpack(formato, buffer)

        monoLeft = samples
    
    with open(ficDer, "rb") as file:
        formato = '<4sI4s'
        buffer = file.read(st.calcsize(formato))
        chunkId, chunkSize, chunkFormat=st.unpack(formato, buffer)

        formato = '<4sIHHIIHH'
        buffer = file.read(st.calcsize(formato))
        subChunk1Id, subChunk1Size, audioFormat, numChannels, sampleRate, byteRate, blockAlign, bitsPerSample=st.unpack(formato, buffer)
        if numChannels != 1:
            raise ValueError("El fichero debe ser mono!")

        formato = '<4sI'
        buffer = file.read(st.calcsize(formato))
        subChunk2Id, subChunk2Size=st.unpack(formato, buffer)

        samplesNumber = int(subChunk2Size // (bitsPerSample // 8))

        formato = f"<{samplesNumber}h"
        buffer = file.read(st.calcsize(formato))
        samples=st.unpack(formato, buffer)

        monoRight = samples

    estereo = [x for par in zip(monoLeft, monoRight) for x in par]

    with open(ficEste, "wb") as file:
        
        formato = '<4sI4s'
        datos = st.pack(formato, chunkId, chunkSize, chunkFormat)
        file.write(datos)
        
        formato = '<4sIHHIIHH'
        datos = st.pack(formato, subChunk1Id, subChunk1Size, audioFormat, 2, sampleRate, sampleRate * 2 * bitsPerSample // 8, 2 * bitsPerSample // 8, bitsPerSample)
        file.write(datos)
        
        formato = '<4sI'
        datos = st.pack(formato, subChunk2Id, len(estereo) * bitsPerSample // 8)
        file.write(datos)
        
        formato = f"<{len(estereo)}h"
        datos = st.pack(formato, *estereo)
        file.write(datos)

def codEstereo(ficEste, ficCod):
"""
Función que lee un fixhero con una señal en estéreo codificada
con un PCM lineal de 16 bits y costruye con esta una codificada con
23 bit que permite la reproducción tanto en mono como en estereo
"""
    with open(ficEste, "rb") as file:
        formato = '<4sI4s'
        buffer = file.read(st.calcsize(formato))
        chunkId, chunkSize, chunkFormat = st.unpack(formato, buffer)

        formato = '<4sIHHIIHH'
        buffer = file.read(st.calcsize(formato))
        (subChunk1Id, subChunk1Size, audioFormat, numChannels, sampleRate, byteRate, blockAlign, bitsPerSample) = st.unpack(formato, buffer)
        if numChannels != 2:
            raise ValueError("El fichero debe ser estéreo")

        formato = '<4sI'
        buffer = file.read(st.calcsize(formato))
        subChunk2Id, subChunk2Size = st.unpack(formato, buffer)
        samplesNumber = subChunk2Size // (bitsPerSample // 8)
        formato = f"<{samplesNumber}h"
        buffer = file.read(st.calcsize(formato))
        samples = st.unpack(formato, buffer)

    left = samples[::2]
    right = samples[1::2]

    codificado = []

    for l, r in zip(left, right):

        suma = (l + r) // 2
        diferencia = (l - r) // 2

        valor32 = ((suma & 0xFFFF) << 16) | (diferencia & 0xFFFF)

        codificado.append(valor32)

    with open(ficCod, "wb") as file:

        subChunk2SizeCod = len(codificado) * 4
        chunkSizeCod = 36 + subChunk2SizeCod

        formato = '<4sI4s'
        datos = st.pack(formato, chunkId, chunkSizeCod, chunkFormat)
        file.write(datos)

        formato = '<4sIHHIIHH'
        datos = st.pack(formato, subChunk1Id, subChunk1Size, audioFormat, 1, sampleRate, sampleRate * 4, 4, 32)
        file.write(datos)

        formato = '<4sI'
        datos = st.pack(formato, subChunk2Id, subChunk2SizeCod)
        file.write(datos)

        formato = f"<{len(codificado)}I"
        datos = st.pack(formato, *codificado)
        file.write(datos)


def decEstereo(ficCod, ficEste):
"""
Función que lee un fichero con una señal mono en 3 bits en la que los
16 más significativos contienen la semisuma de los canales de una 
señal estereo y los 16 menos significativos la semidiferencia, y escribe
un fichero con los dos canales por separado.
"""
    with open(ficCod, "rb") as file:
        formato = '<4sI4s'
        buffer = file.read(st.calcsize(formato))
        chunkId, chunkSize, chunkFormat = st.unpack(formato, buffer)

        formato = '<4sIHHIIHH'
        buffer = file.read(st.calcsize(formato))
        (subChunk1Id, subChunk1Size, audioFormat, numChannels, sampleRate, byteRate, blockAlign, bitsPerSample) = st.unpack(formato, buffer)
        if bitsPerSample != 32:
            raise ValueError("El fichero debe ser mono de 32 bits")

        formato = '<4sI'
        buffer = file.read(st.calcsize(formato))
        subChunk2Id, subChunk2Size = st.unpack(formato, buffer)
        samplesNumber = subChunk2Size // 4
        formato = f"<{samplesNumber}I"
        buffer = file.read(st.calcsize(formato))
        codificado = st.unpack(formato, buffer)

    left = []
    right = []
    for valor32 in codificado:

        suma = (valor32 >> 16) & 0xFFFF
        diferencia = valor32 & 0xFFFF

        # convertir desde complemento a dos
        if suma >= 0x8000:
            suma -= 0x10000

        if diferencia >= 0x8000:
            diferencia -= 0x10000

        l = suma + diferencia
        r = suma - diferencia

        left.append(l)
        right.append(r)

    estereo = [x for par in zip(left, right) for x in par]

    with open(ficEste, "wb") as file:

        subChunk2SizeStereo = len(estereo) * 2
        chunkSizeStereo = 36 + subChunk2SizeStereo

        formato = '<4sI4s'
        datos = st.pack(formato, chunkId, chunkSizeStereo, chunkFormat)
        file.write(datos)

        formato = '<4sIHHIIHH'
        datos = st.pack(formato, subChunk1Id, subChunk1Size, audioFormat, 2, sampleRate, sampleRate * 2 * 2, 2 * 2, 16)
        file.write(datos)

        formato = '<4sI'
        datos = st.pack(formato, subChunk2Id, subChunk2SizeStereo)
        file.write(datos)

        formato = f"<{len(estereo)}h"
        datos = st.pack(formato, *estereo)
        file.write(datos)
