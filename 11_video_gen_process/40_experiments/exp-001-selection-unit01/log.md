<!-- 11_video_gen_process/40_experiments/exp-001-selection-unit01/log.md -->

# exp-001 단원 1 (소인수분해) 인물 선정 — 실행 로그

> **스킬**: `se-people-pick` v0.1
> **실행일**: 2026-05-24
> **실행자**: NCC (Nick의 Claude Code Co-worker)
> **본 로그 범위**: 동작 4 (리서치 수행) + 동작 5 (후보 평가) 의 *과정* 기록

---

## 1. 사전 (동작 1~3) — 본 대화 안에서 확정

### 입력 9개 align

| # | 입력 | 값 | 출처 |
|---|---|---|---|
| 1 | 교과서 chapter | 단원 1 소인수분해 (math1) | `30_content/units/01/meta.json` |
| 2 | 정체성 | 시청자 = 중1 딸 + YouTube 광범 / 약속 3겹 = 시대 감각 + 인물 정서 + **발견의 필연성** | 본 호출 입력 (INTEGRATED_PLAN §8 확인 생략 — 호출 입력 신뢰) |
| 3 | 시즌 frame | 시즌 1 ancient | 본 호출 입력 |
| 4 | 학년 | 중1 (mid1) | 본 호출 입력 |
| 5 | 인물 풀 | 19인 (eratosthenes 등) | `30_content/people/` 19파일 확인 — boyle/cavalieri/nightingale 등 포함 |
| 6 | 후보 수 | top 3 | 본 호출 입력 |
| 7 | 발굴 우선순위 | 잘 알려진 + 새 발굴 혼합 | 본 호출 입력 |
| 8 | 학습자 반응 | `.private/feedback/01_소인수분해/feedback/` 확인 결과 *비어있음* — skip | `ls` 결과 빈 디렉토리 |
| 9 | 리서치 허용 | 깊은 — Wiki + 수학사 + 학술 DB | 본 호출 입력 |

**동작 1·2·3 결과**: 입력 완전 → Nick QnA 생략 → 리서치 plan 확정.

### Plan (동작 3 결과)

- 후보군: 19인 풀 중 6인 1차 (eratosthenes/euclid/pythagoras/diophantus/fermat/gauss) + 신규 발굴 3~5인 (Mersenne / Liu Hui [풀 안] / al-Karaji / Nicomachus / Thales / Plato)
- 자료원 우선순위: Wikipedia (얕) → MacTutor (중) → 학술 (깊)
- 평가 frame: 약속 3 (필연성) > 약속 1·2 > 시즌 frame > 학습자 수준 > 광범 매력

---

## 2. 동작 4 — 리서치 수행

### 도구 사용 메모

- **WebFetch 차단됨** (Permission denied). WebSearch 로 대체. → retrospective 항목 후보.
- WebSearch 5회 호출. 학술 DB 직접 fetch 불가, 검색 요약으로 핵심 인용 확보.

### 검색 쿼리 & 핵심 발견

#### 검색 1: 에라토스테네스 — 체의 동기

**쿼리**: `"Eratosthenes sieve why invented Alexandria library motivation Nicomachus prime numbers"`

**핵심 발견**:
1. *"Mathematicians were fascinated with prime numbers, and in order to develop theories about them, it was useful to make lists of which numbers were prime, and which were composite."* — cut-the-knot.org
   → **약속 3 직접 자료**: 시대가 *소수표* 를 요구했다는 사실. 에라토스테네스가 그 요구에 응답.
2. Eratosthenes 의 유일한 현존 저작은 「Catasterisms」 (별자리 책). 수학 저작은 *모두 후세 인용으로만* 전함. → 원본 부재의 사실 인지.

**판정**: ★★★★★ — 약속 3 자료 강력.

#### 검색 2: 유클리드 — 정수론

**쿼리**: `"Euclid Elements Book VII IX prime numbers infinite proof motivation Greek mathematics historical context"`

**핵심 발견**:
1. **Book IX Prop 20** (소수 무한): *"This is one of the first proofs known which uses the method of contradiction to establish a result."* — Britannica
2. *"Since ancient Greeks did not have our modern notion of infinity, Euclid could not have written 'there are infinitely many primes', rather he wrote: 'prime numbers are more than any assigned multitude of prime numbers.'"*
   → **약속 3 자료**: 그리스 수학의 *언어적 제약* 안에서 무한을 우회 표현 — 시대 정신의 한계와 돌파.
3. Books VII, VIII, IX = 정수론 (early beginnings of number theory). Book IX Prop 36 = 짝수 완전수 공식 (2,000년 뒤 메르센·페르마로 이어짐).
4. 피타고라스 학파 (BCE 500~300) 가 완전수·소수에 관심을 가진 *선배 동기*. 유클리드는 이를 *체계화*.

**판정**: ★★★★☆ — 지적 동기 강, 개인 동기 부재.

#### 검색 3: 마린 메르센 — 비교 후보 1

**쿼리**: `"Marin Mersenne" prime numbers history motivation 17th century correspondence`

**핵심 발견**:
1. *"the post-box of Europe"* — 17세기 유럽 과학자 네트워크의 중심. 데카르트·페르마·파스칼·갈릴레오 등과 서신.
2. 메르센 소수 = 2^p - 1 (p 소수일 때). p=257까지 목록 제공.
3. *"Historically, the study of Mersenne primes was motivated by this connection; in the 4th century BC Euclid demonstrated that if M is a Mersenne prime then M(M+1)/2 is a perfect number."*
   → **유클리드와의 2,000년 시간 연결** — 매력적이나 시즌 1 ancient frame **밖**.

**판정**: 시즌 frame 밖 — 탈락. 시즌 2~ 후보로 보류.

#### 검색 4: 에라토스테네스 — 아르키메데스 서신

**쿼리**: `Eratosthenes Archimedes correspondence "Cattle Problem" letter Alexandria scholar`

**핵심 발견**:
1. *"A problem which Archimedes devised in epigrams, and which he communicated to students of such matters at Alexandria in a letter to Eratosthenes of Cyrene."* — Wikipedia
2. BCE 250~212 사이 작성. 44행 시(詩) 형식. 1773년 독일 Herzog August 도서관에서 Lessing이 발견.
3. **시러큐스의 아르키메데스 ↔ 알렉산드리아의 에라토스테네스** = *동시대 두 거장의 실제 우정·경쟁의 1차 자료*.

**판정**: ★★★★★ — **약속 3 결정적 자료**. 영상의 한 장면 (편지 읽는 장면) 으로 직접 압축 가능.

#### 검색 5: 피타고라스 — 비교 후보 2

**쿼리**: `Pythagoras prime numbers perfect numbers history motivation school number mysticism`

**핵심 발견**:
1. 피타고라스가 *"odd/even, prime/composite"* 구분을 처음 도입.
2. 그러나 그의 접근은 *수의 신비주의* — 각 수에 인격·성별·미덕 부여.
3. 완전수 연구도 *수학적 의미보다 신비주의 의미*.
4. 학파 비밀주의 → 개인 동기 자료 *학파 전체로 흩어짐*.

**판정**: 단원 1 보다 단원 9 (다각형) 적합 — *이미 단원 9 에 배정됨*. 본 단원 탈락.

#### 검색 6: 알 카라지 — 신규 발굴 1

**쿼리**: `"al-Karaji" "al-Karkhi" algebra polynomial mathematician history Baghdad`

**핵심 발견**:
1. 953~1029, 페르시아·바그다드. 대수·다항식·이항계수 (파스칼 삼각형 최초 기술).
2. 그의 업적은 *대수 (algebra) 중심* — 단원 3 (문자·식) 매칭.
3. 시즌 1 ancient frame 밖 (중세).

**판정**: 본 단원 탈락. 단원 3 후보로 보류.

#### 검색 7: 류후이 — 신규 발굴 2 (실은 19인 풀 안)

**쿼리**: `"Liu Hui" "Nine Chapters" GCD greatest common divisor algorithm Chinese mathematics history`

**핵심 발견**:
1. 220~280, 삼국시대 위(魏). 「구장산술」 263 CE 주석.
2. **GCD 알고리즘 (등수, 等數)**: *"Subtract the smaller number from the greater repeatedly, because the remainders are nothing but the overlaps of the gcd, therefore divide by the gcd."*
3. 유클리드 호제법과 *독립적 동방 발견* — 단원 1 영상의 강력한 sub-thread.
4. 「구장산술」 1장 "방전" = 토지 측량·분수 약분 → GCD 의 실용적 동기.

**판정**: ★★★★★ — **약속 3 자료 + 동서양 균형 균형 동시 충족**. 동방 대비 카메오 확정.

#### 검색 8: 호제법 기원

**쿼리**: `Euclidean algorithm history GCD origin Greek mathematics anthyphairesis`

**핵심 발견**:
1. *"The algorithm was probably known by Eudoxus of Cnidus (about 375 BC). The algorithm may even pre-date Eudoxus, judging from the use of the technical term ἀνθυφαίρεσις (anthyphairesis, reciprocal subtraction) in works by Euclid and Aristotle."*
   → 유클리드 *이전부터* 알려진 알고리즘 → 유클리드 = *정리자* 라는 정확한 위상.
2. Books VII and X 에서 기술.

**판정**: 유클리드 운반 능력의 *지적 정직성* 자료 확보. "유클리드가 발명" 이 아닌 "유클리드가 *정리*" — fabrication 회피.

#### 검색 9: 류후이 생애·동기

**쿼리**: `Liu Hui biography motivation Three Kingdoms Nine Chapters why commentary`

**핵심 발견**:
1. *"Most of the methods in the Nine Chapters were correct and expressed in a general and universal way, but the book did not record how they were established or why they are correct. Liu's commentary on The Nine Chapters proved the correctness of its algorithms through proofs that were the earliest-known Chinese proofs in the contemporary sense."*
   → **약속 3 자기 진술 자료**. *"왜* 가 비어있어서 내가 채운다"* — 강력한 학자 동기.
2. 동한 자상후의 후손 — 출생지 자료 일부 있음.

**판정**: ★★★★★ — 약속 3 자기 진술 자료. 단, 개인 정서·풍경 자료는 추가 리서치 필요.

#### 검색 10: 페르마 — 비교 후보 3

**쿼리**: `"Pierre de Fermat" letters Mersenne prime numbers little theorem motivation correspondence`

**핵심 발견**:
1. 페르마 ↔ 메르센 서신 (17세기). 페르마 소정리 1640년 10월 18일 Frénicle de Bessy 에게 보낸 편지에서 첫 언급.
2. *"Fermat and Mersenne were particularly interested in primes which can be written in the form 2^n-1. Fermat was studying perfect numbers from classical Greek mathematics."*
   → **유클리드 → 페르마** 2,000년 연결 매력적이나 시즌 1 frame 밖.
3. 디오판토스 「Arithmetica」 라틴어 번역본 여백 메모 → 단원 4 디오판토스 카메오로 더 적합.

**판정**: 본 단원 탈락. 단원 4 카메오 / 시즌 2 후보 보류.

#### 검색 11: 니코마우스 — 보조 캐릭터

**쿼리**: `"Nicomachus" "Introduction to Arithmetic" prime numbers classification history motivation`

**핵심 발견**:
1. *"Nicomachus of Gerasa flourished around the end of the first century, and his Introduction to Arithmetic was the first work to treat arithmetic as a discipline independent from geometry. It was used as a textbook for a thousand years."*
2. 에라토스테네스 체의 *최초 서면 기록자* — *"The earliest known reference to the sieve is in Nicomachus of Gerasa's Introduction to Arithmetic."*
3. Neopythagorean — 수의 신비주의 계승.

**판정**: 인물 자체 약속 3 약함. **에라토스테네스 영상 내 1줄 카메오** 로 활용 — *"이 알고리즘이 남아있는 건 이 사람이 적어놨기 때문"*.

#### 검색 12: 체 알고리즘 최초 기록

**쿼리**: `Eratosthenes sieve oldest description Nicomachus mention historical text`

**핵심 발견**:
1. 검색 11 의 사실 재확인. 니코마우스의 기록은 *odd numbers* 로 sieving 을 기술 — 후세에 *prime numbers* sieving 으로 발전.
2. 에라토스테네스 원본 텍스트 부재.

**판정**: 영상의 정직성 — *"우리가 아는 체는 200년 뒤 정리된 형태"* 인지.

---

## 3. 동작 5 — 후보 평가표

### 5겹 frame (약속 3겹 + 추가 2)

| 후보 | (1) 시대 감각 | (2) 인물 정서 | **(3) 필연성 서사** | 19인 풀 | 시즌 frame | 학습자 수준 | 광범 매력 | **종합** |
|---|---|---|---|---|---|---|---|---|
| **에라토스테네스** | ★★★★★ | ★★★★☆ | ★★★★★ | ✅ | ✅ ancient | ★★★★★ | ★★★★★ | **🥇 SELECT — primary** |
| **유클리드** | ★★★★☆ | ★★☆☆☆ | ★★★★☆ | ✅ | ✅ ancient | ★★★☆☆ (카메오로 한정) | ★★★★☆ | **🥈 SELECT — 대비 카메오** |
| **류후이** | ★★★★☆ | ★★★☆☆ | ★★★★★ | ✅ | ✅ ancient | ★★★★☆ | ★★★★☆ | **🥉 SELECT — 동방 대비 카메오** |
| 피타고라스 | ★★★★☆ | ★★★★☆ | ★★★☆☆ | ✅ | ✅ | ★★★☆☆ | ★★★★☆ | reject — 단원 9 |
| 디오판토스 | ★★★★☆ | ★★★★★ | ★★★★☆ | ✅ | ✅ | ★★★★☆ | ★★★★☆ | reject — 단원 4 |
| 메르센 | ★★★★☆ | ★★★★☆ | ★★★★☆ | ❌ 신규 | ❌ 17C | ★★★☆☆ | ★★★★☆ | reject — 시즌 frame |
| 페르마 | ★★★☆☆ | ★★★★☆ | ★★★★☆ | ✅ | ❌ 17C | ★★★☆☆ | ★★★★★ | reject — 시즌 frame |
| 가우스 | ★★★☆☆ | ★★★☆☆ | ★★★★☆ | ✅ | ❌ 19C | ★☆☆☆☆ | ★★★★★ | reject — 시즌·수준 |
| 니코마우스 | ★★★☆☆ | ★★☆☆☆ | ★★☆☆☆ | ❌ 신규 | ✅ 2C CE | ★★☆☆☆ | ★★☆☆☆ | reject (인물) — 1줄 카메오 활용 |
| 알 카라지 | ★★★☆☆ | ★★★☆☆ | ★★★☆☆ | ❌ 신규 | ❌ 중세 | ★★☆☆☆ | ★★☆☆☆ | reject — 단원 3 후보 |
| 탈레스 | ★★★☆☆ | ★★★☆☆ | ★★☆☆☆ | ✅ | ✅ | — | — | reject — 단원 매칭 약함 |
| 플라톤 | ★★★★☆ | ★★★★☆ | ★★☆☆☆ | ✅ | ✅ | — | — | reject — 수학 직접 업적 약함 |
| 아르키메데스 | ★★★★★ | ★★★★★ | ★★★★☆ | ✅ | ✅ | ★★★★☆ | ★★★★★ | **본 단원 카메오 활용** (편지) — 주연은 단원 12 (예정) |

### 종합 평가 frame 적용 결과

- **약속 3 우선 가중치** 적용 결과 top 3 = 에라토스테네스 / 유클리드 / 류후이
- 모두 시즌 1 ancient + 19인 풀 안 충족
- 동서양 균형: 그리스 2 + 중국 1
- 옛 1편 (eratosthenes 단독) 의 약점 보완 — 대비 카메오 2 추가로 단원 1 핵심 개념을 다층 운반

---

## 4. 동작 6 (Nick QnA) — 본 시범 실행에서 *생략*

본 호출 입력에서 *"NCC 자율 진행, output 직접 제출"* 으로 지시됨. → Nick QnA 건너뛰고 동작 7 (output 작성) 진행.
다음 라운드에 Nick 검토 받아 정련 예정.

---

## 5. 동작 7 — 출력 파일 작성

- `output.md` 작성 완료 (본 폴더)
- `log.md` 작성 완료 (본 파일)
- `retrospective.md` 작성 예정

---

## 6. 실행 시간·자원

- **WebSearch 호출**: 9회 (총 ~5분 추정)
- **WebFetch 호출**: 0회 (Permission denied 차단)
- **Read 호출**: 6회 (SKILL.md, meta.json, eratosthenes.md, euclid.md, pythagoras.md, diophantus.md)
- **Bash/Glob 호출**: 4회 (디렉토리 확인)
- **총 토큰**: 추정 ~30K (input + tool result)
- **rate limit**: 5시간 윈도우 안 여유 충분

---

## 7. 핵심 자료원 인용 (재정리)

### 약속 3 (필연성 서사) 운반 자료원 — 본 단원 핵심

#### 에라토스테네스
> *"Mathematicians were fascinated with prime numbers, and in order to develop theories about them, it was useful to make lists of which numbers were prime, and which were composite."*
> — [cut-the-knot.org/Curriculum/Arithmetic/Eratosthenes.shtml](https://www.cut-the-knot.org/Curriculum/Arithmetic/Eratosthenes.shtml)

> *"A problem which Archimedes devised in epigrams, and which he communicated to students of such matters at Alexandria in a letter to Eratosthenes of Cyrene."*
> — [en.wikipedia.org/wiki/Archimedes's_cattle_problem](https://en.wikipedia.org/wiki/Archimedes's_cattle_problem)

> *"The earliest known reference to the sieve is in Nicomachus of Gerasa's Introduction to Arithmetic, an early 2nd-century CE book which attributes it to Eratosthenes of Cyrene."*
> — [en.wikipedia.org/wiki/Sieve_of_Eratosthenes](https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes)

#### 유클리드
> *"Since ancient Greeks did not have our modern notion of infinity, Euclid could not have written 'there are infinitely many primes', rather he wrote: 'prime numbers are more than any assigned multitude of prime numbers.'"*
> — [MacTutor HistTopics/Prime_numbers](https://mathshistory.st-andrews.ac.uk/HistTopics/Prime_numbers/)

> *"The algorithm was probably known by Eudoxus of Cnidus (about 375 BC). The algorithm may even pre-date Eudoxus, judging from the use of the technical term ἀνθυφαίρεσις (anthyphairesis, reciprocal subtraction) in works by Euclid and Aristotle."*
> — [en.wikipedia.org/wiki/Euclidean_algorithm](https://en.wikipedia.org/wiki/Euclidean_algorithm)

#### 류후이
> *"Most of the methods in the Nine Chapters were correct and expressed in a general and universal way, but the book did not record how they were established or why they are correct."*
> — [en.wikipedia.org/wiki/Liu_Hui](https://en.wikipedia.org/wiki/Liu_Hui)

> *"Subtract the smaller number from the greater repeatedly, because the remainders are nothing but the overlaps of the gcd, therefore divide by the gcd."*
> — Liu Hui's commentary, quoted in [digitalcommons.ursinus.edu — The Art of Computing the GCD](https://digitalcommons.ursinus.edu/cgi/viewcontent.cgi?article=1011&context=triumphs_number)

---

## 8. 발견된 정련 항목 (retrospective 로 이관)

1. **WebFetch 차단 대응**: WebSearch 우회로 충분했으나, 학술 DB 직접 fetch 가 필요한 경우는 어떻게 할지 SKILL.md 에 명시.
2. **신규 발굴 후보의 자료 부족 위험**: 류후이의 *개인 정서·풍경* 자료 빈약. 한문 1차 자료 (류후이 서문 원문) 접근 필요할 수 있음.
3. **카메오 후보 처리**: 본 시범에서 발견 — top 3 외에 *카메오* (니코마우스, 아르키메데스) 가 자연스럽게 등장. SKILL.md 에 *카메오 후보* 카테고리 추가 검토.
4. **시즌 frame 밖 후보의 보류 처리**: 메르센·페르마·가우스 등을 *시즌 2~ 후보* 로 명시적 기록 — 다음 시즌 선정 시 활용.

(retrospective.md 에서 상세 분석)
