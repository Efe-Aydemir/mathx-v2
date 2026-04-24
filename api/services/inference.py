"""
Inference service for communicating with the vLLM server via OpenAI-compatible API.
Includes both real inference and mock mode for local development.
"""

import asyncio
from typing import AsyncGenerator

from openai import AsyncOpenAI

from config import settings
from prompts.system_prompts import get_system_prompt, format_user_prompt


# Initialize the OpenAI client pointing to vLLM
client = AsyncOpenAI(
    base_url=settings.VLLM_BASE_URL,
    api_key=settings.VLLM_API_KEY,
)


async def stream_inference(
    category: str,
    subcategory: str,
    question: str,
) -> AsyncGenerator[str, None]:
    """
    Stream token-by-token inference from the vLLM server.

    Yields text chunks as they arrive from the model.
    """
    system_prompt = get_system_prompt(category)
    user_message = format_user_prompt(category, subcategory, question)

    try:
        stream = await client.chat.completions.create(
            model=settings.VLLM_MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            stream=True,
            temperature=0.3,
            max_tokens=4096,
            top_p=0.9,
        )

        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    except Exception as e:
        yield f"\n\n⚠️ Model bağlantı hatası: {str(e)}"


# ===== Mock Mode =====

MOCK_SOLUTIONS: dict[str, str] = {
    "Soyut Matematik": """## Çözüm

**Verilen:** Problem analiz ediliyor...

**Adım 1: Tanımları Kontrol Edelim**

Bir $R$ bağıntısının denklik bağıntısı olabilmesi için üç koşulu sağlaması gerekir:

1. **Refleksif (Yansıma):** Her $a \\in A$ için $(a, a) \\in R$ olmalıdır.
2. **Simetrik:** Her $(a, b) \\in R$ için $(b, a) \\in R$ olmalıdır.
3. **Geçişli (Transitif):** Her $(a, b), (b, c) \\in R$ için $(a, c) \\in R$ olmalıdır.

**Adım 2: Refleksif Özellik Kontrolü**

$$\\forall a \\in A: (a, a) \\in R$$

Kontrol ediyoruz: $(1,1) \\in R$ ✓, $(2,2) \\in R$ ✓, $(3,3) \\in R$ ✓

Refleksif özellik sağlanıyor. ✓

**Adım 3: Simetrik Özellik Kontrolü**

Her $(a,b) \\in R$ için $(b,a) \\in R$ olmalı:

$(1,2) \\in R \\Rightarrow (2,1) \\in R$ ✓

Simetrik özellik sağlanıyor. ✓

**Adım 4: Geçişli Özellik Kontrolü**

$$\\forall (a,b), (b,c) \\in R \\Rightarrow (a,c) \\in R$$

Kontrol ediyoruz: $(1,2) \\in R$ ve $(2,1) \\in R \\Rightarrow (1,1) \\in R$ ✓

Geçişli özellik sağlanıyor. ✓

---

**Sonuç:** Verilen bağıntı bir **denklik bağıntısıdır** çünkü refleksif, simetrik ve geçişli özelliklerin üçünü de sağlamaktadır. ✅""",

    "Lineer Cebir": """## Çözüm

**Verilen:** Problem analiz ediliyor...

**Adım 1: Problemi Formüle Edelim**

Verilen vektörlerin lineer bağımsızlığını kontrol etmek için, aşağıdaki denklemi inceleyelim:

$$c_1 \\mathbf{v}_1 + c_2 \\mathbf{v}_2 + c_3 \\mathbf{v}_3 = \\mathbf{0}$$

Bu denklemin yalnızca $c_1 = c_2 = c_3 = 0$ trivial çözümüne sahip olup olmadığını kontrol edeceğiz.

**Adım 2: Matris Formuna Geçiş**

Vektörleri bir matrisin sütunlarına yerleştirelim:

$$A = \\begin{pmatrix} 1 & 4 & 7 \\\\ 2 & 5 & 8 \\\\ 3 & 6 & 9 \\end{pmatrix}$$

**Adım 3: Satır İndirgemesi (Gauss Eliminasyonu)**

$$R_2 \\leftarrow R_2 - 2R_1, \\quad R_3 \\leftarrow R_3 - 3R_1$$

$$\\begin{pmatrix} 1 & 4 & 7 \\\\ 0 & -3 & -6 \\\\ 0 & -6 & -12 \\end{pmatrix}$$

$$R_3 \\leftarrow R_3 - 2R_2$$

$$\\begin{pmatrix} 1 & 4 & 7 \\\\ 0 & -3 & -6 \\\\ 0 & 0 & 0 \\end{pmatrix}$$

**Adım 4: Yorumlama**

Son satır tamamen sıfır olduğundan, matrisin rankı $\\text{rank}(A) = 2 < 3$ (vektör sayısı).

Bu, denklemin sıfırdan farklı çözümlere sahip olduğunu gösterir.

---

**Sonuç:** Vektörler **lineer bağımlıdır** çünkü $\\text{rank}(A) = 2 < 3$. Sıfır olmayan katsayılarla birbirlerinin lineer birleşimi olarak yazılabilirler:

$$\\mathbf{v}_3 = 2\\mathbf{v}_2 - \\mathbf{v}_1$$ ✅""",

    "Çizge Teorisi": """## Çözüm

**Verilen:** Problem analiz ediliyor...

**Adım 1: El Sıkışma Lemmasını Kullanalım**

El sıkışma lemmasına göre:

$$\\sum_{v \\in V} \\deg(v) = 2|E|$$

**Adım 2: Hesaplama**

6 düğümlü grafta her düğümün derecesi 3 ise:

$$\\sum_{v \\in V} \\deg(v) = 6 \\times 3 = 18$$

Dolayısıyla:

$$2|E| = 18 \\Rightarrow |E| = 9$$

**Sonuç:** Grafın **9 kenarı** vardır. ✅""",

    "Topoloji": """## Çözüm

**Verilen:** Problem analiz ediliyor...

**Adım 1: Topoloji Aksiyomlarını Kontrol Edelim**

$\\tau$ ailesinin bir topoloji olabilmesi için:

1. $\\emptyset \\in \\tau$ ve $X \\in \\tau$ olmalıdır.
2. $\\tau$'deki herhangi sayıda kümenin birleşimi $\\tau$'da olmalıdır.
3. $\\tau$'deki sonlu sayıda kümenin kesişimi $\\tau$'da olmalıdır.

**Adım 2: Aksiyom 1 Kontrolü**

$\\emptyset \\in \\tau$ ✓ ve $X = \\{a, b, c\\} \\in \\tau$ ✓

**Adım 3: Aksiyom 2 — Birleşim Kapalılığı**

Tüm olası birleşimleri kontrol edelim:
- $\\emptyset \\cup \\{a\\} = \\{a\\} \\in \\tau$ ✓
- $\\{a\\} \\cup \\{a,b\\} = \\{a,b\\} \\in \\tau$ ✓
- $\\emptyset \\cup \\{a,b\\} = \\{a,b\\} \\in \\tau$ ✓

Birleşim kapalılığı sağlanıyor. ✓

**Adım 4: Aksiyom 3 — Kesişim Kapalılığı**

$$\\{a\\} \\cap \\{a,b\\} = \\{a\\} \\in \\tau \\checkmark$$

Kesişim kapalılığı sağlanıyor. ✓

---

**Sonuç:** $\\tau = \\{\\emptyset, \\{a\\}, \\{a,b\\}, X\\}$ ailesi bir **topolojidir** çünkü tüm aksiyomları sağlamaktadır. ✅""",
}


async def stream_mock_inference(
    category: str,
    subcategory: str,
    question: str,
) -> AsyncGenerator[str, None]:
    """
    Mock inference that simulates streaming by yielding characters with a delay.
    Used for local development without GPU access.
    """
    solution = MOCK_SOLUTIONS.get(category, MOCK_SOLUTIONS["Soyut Matematik"])

    # Simulate token-by-token streaming
    words = solution.split(" ")
    for i, word in enumerate(words):
        if i > 0:
            yield " "
        yield word
        # Variable delay to simulate real inference
        delay = 0.02 if len(word) < 3 else 0.04
        await asyncio.sleep(delay)
