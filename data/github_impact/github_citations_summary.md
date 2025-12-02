# GitHub Citations of johndcook.com

**Search Date:** 2025-12-01
**Total Unique Repositories:** 160

---

## Notable High-Profile Citations

These repositories cite johndcook.com in their code, documentation, or references:

### Tier 1: Foundational Data Science Infrastructure (40k+ stars)

| Repository | Stars | Citation Context |
|------------|-------|------------------|
| [EbookFoundation/free-programming-books](https://github.com/EbookFoundation/free-programming-books) | 378,061 | Lists Cook's resources in programming books collection |
| [JuliaLang/julia](https://github.com/JuliaLang/julia) | 48,023 | References Cook's blog in floating-point documentation |
| [pandas-dev/pandas](https://github.com/pandas-dev/pandas) | 47,223 | Cites Cook's interpolation methods in `groupby.pyx` |

### Tier 2: Major ML/Scientific Computing (5k-10k stars)

| Repository | Stars | Citation Context |
|------------|-------|------------------|
| [tensorflow/docs](https://github.com/tensorflow/docs) | 6,275 | "Don't invert that matrix" in autodiff guide |
| [OpenTSDB/opentsdb](https://github.com/OpenTSDB/opentsdb) | 5,060 | Cook's aggregation methods in `Aggregators.java` |
| [stan-dev/stan](https://github.com/stan-dev/stan) | 4,584 | Statistical references |

### Tier 3: Respected Scientific Libraries (1k-5k stars)

| Repository | Stars | Citation Context |
|------------|-------|------------------|
| [mwaskom/seaborn](https://github.com/mwaskom/seaborn) | 3,162 | Statistical visualization |
| [pymc-devs/pymc](https://github.com/pymc-devs/pymc) | 2,907 | Probabilistic programming |
| [jeroenjanssens/data-science-at-the-command-line](https://github.com/jeroenjanssens/data-science-at-the-command-line) | 4,700+ | Acknowledges Cook |
| [mathnet/mathnet-numerics](https://github.com/mathnet/mathnet-numerics) | 3,500+ | Cook listed as contributor |
| [plasma-umass/coz](https://github.com/plasma-umass/coz) | 4,000+ | Uses Cook's science.js |

### Tier 4: Specialized Technical Libraries

| Repository | Context |
|------------|---------|
| [python/peps](https://github.com/python/peps) | PEP 450 cites Cook's statistics work |
| [microsoft/BuildXL](https://github.com/microsoft/BuildXL) | Cook's algorithms in cache utilities |
| [CoolProp/CoolProp](https://github.com/CoolProp/CoolProp) | Thermodynamics library uses Cook's numerics |
| [Unity-Technologies/com.unity.perception](https://github.com/Unity-Technologies/com.unity.perception) | Sampler utilities |
| [AllenDowney/ThinkBayes2](https://github.com/AllenDowney/ThinkBayes2) | Bayesian statistics textbook |

---

## Citation Patterns by Topic

### Gamma Function Implementations
Cook's gamma function approximation appears in:
- C# (Gamma.cs)
- Java (MathEngine)
- PHP (NlpTools)
- C++ (multiple libraries)
- JavaScript (mathfn, Hurmet)
- PowerShell (Get-Gamma.ps1)
- Rust (quadrature)

### "Don't Invert That Matrix"
This post has become a canonical teaching reference, cited in:
- TensorFlow documentation
- QuantEcon lectures
- NYU Data Science coursework
- Multiple linear algebra tutorials
- Gaussian process implementations

### Random Number Generation
Cook's random distribution implementations referenced in:
- Gauche Scheme
- D language (turtle)
- Nim (alea)
- Julia (BayesianMixtures, QuantumControlTestUtils)
- Fortran (ARVE-Research/BIOME)

### Interpolation Methods
Cited in pandas core (`groupby.pyx`) and numerous scientific computing libraries.

---

## Evidence Categories

### 1. Code Comments Citing Source
```python
# pandas/_libs/groupby.pyx
# Reference: johndcook.com/blog on interpolation
```

### 2. Documentation References
```markdown
# tensorflow/docs/advanced_autodiff.ipynb
See [Don't invert that matrix](https://www.johndcook.com/blog/2010/01/19/dont-invert-that-matrix/)
```

### 3. Implementation Attributions
```csharp
// Based on John D. Cook's gamma function approximation
// https://www.johndcook.com/blog/gamma_function/
```

### 4. Reading Lists & Resources
Free Programming Books, awesome lists, and course materials frequently recommend Cook's blog.

---

## Key Findings for Book

1. **Production Code**: Cook's algorithms run in pandas (47k stars) - one of the most-used data science libraries in the world.

2. **Language Documentation**: Julia's official docs cite Cook for floating-point explanations.

3. **ML Infrastructure**: TensorFlow's official documentation links to "Don't invert that matrix."

4. **Teaching Canon**: "Don't invert that matrix" has become standard reading in numerical linear algebra courses.

5. **Cross-Language Impact**: Implementations of Cook's code exist in Python, R, Julia, C++, C#, Java, JavaScript, Rust, Fortran, Scheme, Nim, D, and PowerShell.

6. **Contributor Credit**: Cook is listed as a contributor to mathnet-numerics, a major .NET numerics library.

---

## Raw Data

Full results saved in:
- `code_search_results.json` (160 entries)
- `repos_mentioning_johndcook.json` (API results)
