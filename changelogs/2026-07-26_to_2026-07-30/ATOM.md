# ATOM: PR digest (2026-07-26 to 2026-07-30)

_33 merged, 15 newly opened - source ROCm/ATOM, generated 2026-07-30T11:28:03Z_

## TL;DR
- **DeepSeek-V4 and Kimi-K3** dominated this window. DeepSeek-V4 gained native API support, FP4 indexers, and in-flight work on an elastic unified-KV arena. Kimi-K3 received Day 0 main support across ATOM and vLLM plugins.
- **Speculative Decoding** saw a major refactor to the DSpark drafter abstraction, aligning it with the HuggingFace reference and boosting acceptance rates from 34.9% to 48%.
- **Distributed Serving** expanded significantly with the introduction of Chunked Pipeline Parallelism, Prefill/Decode (PD) Disaggregation, and Atomesh integration.
- **MLA Distributed Cache Parallelism (DCP)** was optimized to enable Prefix Caching, Chunked Prefill, and FP8 KV Cache, drastically reducing memory overhead.
- **Overall direction** focuses on scaling out large model serving via advanced parallelism (DCP, PD disaggregation) and tighter integration with the vLLM and SGLang ecosystems.

## Most important PRs
- **[#1700](https://github.com/ROCm/ATOM/pull/1700)** refactors the DSpark speculative decoding drafter abstraction to align with the HuggingFace reference, increasing the acceptance rate from 34.9% to 48%.
- **[#1552](https://github.com/ROCm/ATOM/pull/1552)** introduces Chunked Pipeline Parallelism, Prefill/Decode (PD) Disaggregation, and Atomesh support, enabling highly decoupled and scalable distributed serving.
- **[#1718](https://github.com/ROCm/ATOM/pull/1718)** adds Day 0 main support for the Kimi-K3 architecture, including its specific MLA and MoE components.
- **[#1701](https://github.com/ROCm/ATOM/pull/1701)** optimizes MLA Distributed Cache Parallelism (DCP) by enabling Prefix Caching, Chunked Prefill, and FP8 KV Cache to minimize memory bottlenecks.
- **[#1704](https://github.com/ROCm/ATOM/pull/1704)** (newly opened) proposes an elastic unified-KV arena for DeepSeek-V4 that fuses Cross-Sequence Attention (CSA) boundary state into the Sliding Window Attention (SWA) block.

## More changes by area

<details>
<summary>MoE & quantization (3)</summary>

- [#1708](https://github.com/ROCm/ATOM/pull/1708) fixes the batched MoE staging path by enforcing an explicit ownership rule
- [#1709](https://github.com/ROCm/ATOM/pull/1709) adds an FP4 indexer for DeepSeek-V4
- [#1715](https://github.com/ROCm/ATOM/pull/1715) keeps EPLB for pure prefill and optimizes remap and record operations

</details>

<details>
<summary>Model support (4)</summary>

- [#1733](https://github.com/ROCm/ATOM/pull/1733) adds DSpark support for Kimi-K3
- [#1735](https://github.com/ROCm/ATOM/pull/1735) supports Kimi-K3 in the vLLM plugin mode
- [#1680](https://github.com/ROCm/ATOM/pull/1680) enables Prefix Cache (PCP) in SGLang ATOM for GLM-5.2
- [#1738](https://github.com/ROCm/ATOM/pull/1738) (newly opened) adds support for the Qwen3.5x model family

</details>

<details>
<summary>Parallelism & scheduling (6)</summary>

- [#1681](https://github.com/ROCm/ATOM/pull/1681) overlaps pure-TP all_reduce on TBO and delays Tensor Parallelism for DeepSeek-V4
- [#1682](https://github.com/ROCm/ATOM/pull/1682) enables index_share_for_mtp_iteration in the native MTP EagleProposer
- [#1647](https://github.com/ROCm/ATOM/pull/1647) fixes PD decode admission caps and remote-KV backpressure
- [#1737](https://github.com/ROCm/ATOM/pull/1737) enables FP8 2-buffer KV transfer for PD disaggregation on DeepSeek-V4
- [#1746](https://github.com/ROCm/ATOM/pull/1746) (newly opened) switches DCP decode to persistent PageAttention and makes DCP compatible with MTP
- [#1743](https://github.com/ROCm/ATOM/pull/1743) (newly opened) adds MTP support for blocksizes other than 1

</details>

<details>
<summary>API & serving (7)</summary>

- [#1741](https://github.com/ROCm/ATOM/pull/1741) implements DeepSeek-V4 native OpenAI/Anthropic/Responses API and DSML tool parser
- [#1585](https://github.com/ROCm/ATOM/pull/1585) updates the ATOM SGLang plugin for SGLang 0.5.15.post1
- [#1587](https://github.com/ROCm/ATOM/pull/1587) upgrades the vLLM plugin to v0.25.1
- [#1747](https://github.com/ROCm/ATOM/pull/1747) (newly opened) supports the GLM-5.2 tool call parser
- [#1706](https://github.com/ROCm/ATOM/pull/1706) (newly opened) adds a chat template
- [#1705](https://github.com/ROCm/ATOM/pull/1705) adds the served model name to responses
- [#1711](https://github.com/ROCm/ATOM/pull/1711) fixes streaming usage chunks by adding an empty choices field

</details>

<details>
<summary>Hardware & arch (1)</summary>

- [#1719](https://github.com/ROCm/ATOM/pull/1719) (newly opened) adds MI455 support for Kimi-K3

</details>

<details>
<summary>Kernels & attention (1)</summary>

- [#1359](https://github.com/ROCm/ATOM/pull/1359) adds a dtype option to the LayerNorm class

</details>

<details>
<summary>Bugfixes (10)</summary>

- [#1744](https://github.com/ROCm/ATOM/pull/1744) fixes a DSpark piecewise cudagraph accuracy issue at 512 concurrency
- [#1710](https://github.com/ROCm/ATOM/pull/1710) defers streaming chat role chunks until generation starts
- [#1717](https://github.com/ROCm/ATOM/pull/1717) validates cached accuracy model shards in SGLang
- [#1729](https://github.com/ROCm/ATOM/pull/1729) falls back when HuggingFace cache roots are unwritable
- [#1727](https://github.com/ROCm/ATOM/pull/1727) (newly opened) applies multiple fixes to pass Kimi-K3 KVV
- [#1725](https://github.com/ROCm/ATOM/pull/1725) (newly opened) fixes LM cache write-back
- [#1742](https://github.com/ROCm/ATOM/pull/1742) (newly opened) recycles post-final-norm hidden states between MTP draft steps
- [#1739](https://github.com/ROCm/ATOM/pull/1739) (newly opened) fixes DeepSeek-V4 FP8 block128 on MI308
- [#1731](https://github.com/ROCm/ATOM/pull/1731) (newly opened) fixes the DeepSeek-V4 FP8 compressor
- [#1707](https://github.com/ROCm/ATOM/pull/1707) (newly opened) back-fills deferred-output placeholders before overwrite to prevent IndexError crashes

</details>

<details>
<summary>CI & build (8)</summary>

- [#1740](https://github.com/ROCm/ATOM/pull/1740) (newly opened) supports SWE-bench lite precision validation
- [#1675](https://github.com/ROCm/ATOM/pull/1675) adds CI cases and recipes for the GLM-5.2 agentic benchmark
- [#1730](https://github.com/ROCm/ATOM/pull/1730) supports the Crusoe cluster and aligns the serving benchmark script
- [#1726](https://github.com/ROCm/ATOM/pull/1726) adds an Agentic Trace item under ISL/OSL
- [#1721](https://github.com/ROCm/ATOM/pull/1721) fixes GLM-5.2 FP8 MI308 CI by removing online quantization
- plus 3 more minor CI updates for benchmark schedules and Atomesh MTP cases ([#1745](https://github.com/ROCm/ATOM/pull/1745), [#1728](https://github.com/ROCm/ATOM/pull/1728), [#1734](https://github.com/ROCm/ATOM/pull/1734))

</details>

<details>
<summary>Docs (2)</summary>

- [#1692](https://github.com/ROCm/ATOM/pull/1692) adds explanations for online and offline quantization
- [#1732](https://github.com/ROCm/ATOM/pull/1732) adds the Kimi-K3 Day 0 AMD developer article to News

</details>

<details>
<summary>Tests (1)</summary>

- [#1723](https://github.com/ROCm/ATOM/pull/1723) (newly opened) adds a block-level DeepSeek-V4 attention test

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (ATOM.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 74c346e061cfb243558fa1cca90197446ad911137007e289a3068b65a58ebf9f -->
