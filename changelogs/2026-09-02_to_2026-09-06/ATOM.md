# ATOM: PR digest (2026-09-02 to 2026-09-06)

_19 merged, 20 newly opened - source ROCm/ATOM, generated 2026-09-06T23:16:00Z_

## TL;DR
- **Kimi-K3 and DeepSeek (DSA/DSV4) dominated the window.** Merged work covered K3 LMCache offload, fused KDA kernels and fused act+fp8 per-token quant. DeepSeek work centered on DCP (decode context parallel) top-k merge, MTP-compatible indexer scoring, and PCP+MTP fixes. GLM-5.3-Flash landed in text form on MI355X.
- **The main perf work was in MLA and DCP decode.** It includes a fused prefill context reorg + dequant + kv_b_proj kernel with custom AllGather (`[#2113](https://github.com/ROCm/ATOM/pull/2113)`), the query-head pad folded into the fused q write (`[#2120](https://github.com/ROCm/ATOM/pull/2120)`), and a fused DCP top-k merge (`[#2087](https://github.com/ROCm/ATOM/pull/2087)`).
- **MoE and speculative decoding got infrastructure.** A native RCCL DEP transport merged. DP-vocab-sharded greedy argmax for drafting merged. Open PRs add AITer comm-fused MoE for DSV4 and DSpark spec-decode.
- **Direction:** long-context KV offload (LMCache for K3, GLM-5.2 and MiniMax-M3), DCP/PCP parallelism with MTP, and a large KV-pool refactor (`[#2147](https://github.com/ROCm/ATOM/pull/2147)`). CI hardening runs alongside.

## Most important PRs
**[#2053](https://github.com/ROCm/ATOM/pull/2053) — Kimi-K3 LMCache offload**
This is the largest merged change (+10k lines). It adds KV offload for K3's attention and MLA through the plugin and distributed layers, with tests and docs. It is the base for the follow-on LMCache work for GLM-5.2 and MiniMax-M3.

**[#2051](https://github.com/ROCm/ATOM/pull/2051) — GLM-5.3-Flash text path on MI355X**
It adds GLM-5.3-Flash (glm5_next) end to end: MLA attention, MoE, and the aiter and Triton backends. Tests and CI are included. A multimodal follow-up is open as `[#2141](https://github.com/ROCm/ATOM/pull/2141)`.

**[#2110](https://github.com/ROCm/ATOM/pull/2110) — Native RCCL DEP transport for MoE**
It adds a native RCCL transport for DEP MoE dispatch/combine, removing the dependence on an external communication backend. Tests and CI are included.

**[#2118](https://github.com/ROCm/ATOM/pull/2118) — Per-query-token sparse decode indexer scoring (DSA/DCP)**
The indexer now scores each query token, which unblocks MTP with DCP. `[#2087](https://github.com/ROCm/ATOM/pull/2087)` complements it with an opt-in fused DCP decode top-k merge.

**[#2089](https://github.com/ROCm/ATOM/pull/2089) — Fused activation + fp8 per-token quant for K3**
It fuses activation and fp8 per-token quantization in Triton for dense/shared MLP and full attention. This removes separate quant passes in the K3 hot path.

## More changes by area

<details>
<summary>Performance (3)</summary>

- [#2113](https://github.com/ROCm/ATOM/pull/2113) fuse prefill context reorg, dequant and kv_b_proj into one kernel, using the custom AllGather
- [#2120](https://github.com/ROCm/ATOM/pull/2120) fold the MLA query-head pad into the fused q write
- [#1965](https://github.com/ROCm/ATOM/pull/1965) fuse kernels in KDA

</details>

<details>
<summary>Kernels & attention (2)</summary>

- [#2139](https://github.com/ROCm/ATOM/pull/2139) derive a prefill step's token indices without a Python loop
- [#2087](https://github.com/ROCm/ATOM/pull/2087) opt-in fused DCP decode top-k merge for DSA

</details>

<details>
<summary>MoE & quantization (1)</summary>

- [#2095](https://github.com/ROCm/ATOM/pull/2095) route gfx1250 wo_a grouped LoRA through the FlyDSL A8W8 BMM

</details>

<details>
<summary>Parallelism & scheduling (1)</summary>

- [#2128](https://github.com/ROCm/ATOM/pull/2128) DP-vocab-sharded greedy argmax for speculative drafting

</details>

<details>
<summary>Bugfixes (1)</summary>

- [#2049](https://github.com/ROCm/ATOM/pull/2049) fix DSV4 PCP with MTP

</details>

<details>
<summary>CI & build (4)</summary>

- [#2115](https://github.com/ROCm/ATOM/pull/2115) change the atom-plugin CI runner label
- [#2099](https://github.com/ROCm/ATOM/pull/2099) prevent benchmark dashboard history loss
- [#2143](https://github.com/ROCm/ATOM/pull/2143) retry docker push, gate manual dashboard uploads, set ATOM_MOE_GU_ITLV on gpt-oss
- [#2135](https://github.com/ROCm/ATOM/pull/2135) drop the Llama-3-8B-Instruct accuracy test

</details>

<details>
<summary>Other (2)</summary>

- [#1919](https://github.com/ROCm/ATOM/pull/1919) integrate the aiter fused KDA decode kernel for K3
- [#2133](https://github.com/ROCm/ATOM/pull/2133) revert [#1919](https://github.com/ROCm/ATOM/pull/1919)

</details>

<details>
<summary>Newly opened: Model support & features (8)</summary>

- [#2131](https://github.com/ROCm/ATOM/pull/2131) Kimi-K3 AgentX recipe
- [#2137](https://github.com/ROCm/ATOM/pull/2137) enable DSpark speculative decoding for DeepSeek-V4-Flash-0731 on atom-vllm
- [#2142](https://github.com/ROCm/ATOM/pull/2142) LMCache offload for GLM-5.2 on atom-vllm
- [#2146](https://github.com/ROCm/ATOM/pull/2146) MiniMax-M3 byte-level KV offload driven from the vLLM plugin
- [#2140](https://github.com/ROCm/ATOM/pull/2140) PAGE-only m3 layout for MiniMax-M3 kv_transfer/offload
- [#2141](https://github.com/ROCm/ATOM/pull/2141) GLM-5.3-Flash multimodal support
- [#2114](https://github.com/ROCm/ATOM/pull/2114) AITer communication-fused MoE for DSV4
- [#2116](https://github.com/ROCm/ATOM/pull/2116) capture DeepSeek-V4 MTP step zero (perf)

</details>

<details>
<summary>Newly opened: Parallelism, serving & perf (4)</summary>

- [#2121](https://github.com/ROCm/ATOM/pull/2121) MLA/Indexer cache transfer for P-CPP/D-DCP PD scenario
- [#2125](https://github.com/ROCm/ATOM/pull/2125) shard `shared_experts` on the folded TP grid for PCP, and sync sampled ids outside the speculative branch
- [#2112](https://github.com/ROCm/ATOM/pull/2112) define a profiler window
- [#2130](https://github.com/ROCm/ATOM/pull/2130) make the K3 KDA temporal state dtype configurable

</details>

<details>
<summary>Newly opened: Refactors (2)</summary>

- [#2147](https://github.com/ROCm/ATOM/pull/2147) one declaration per fact about the KV pools
- [#2132](https://github.com/ROCm/ATOM/pull/2132) refactor K3 LMCache (marked NOT READY)

</details>

<details>
<summary>Newly opened: Bugfixes & CI (5)</summary>

- [#2138](https://github.com/ROCm/ATOM/pull/2138) commit Cargo.lock for atom/mesh, unblocking image builds broken by tinyvec 1.13.0
- [#2122](https://github.com/ROCm/ATOM/pull/2122) unblock fp8 KV cache and EAGLE3 spec decode for MiniMax-M3 on the vLLM plugin
- [#2126](https://github.com/ROCm/ATOM/pull/2126) fix K3 piecewise cudagraph
- [#2129](https://github.com/ROCm/ATOM/pull/2129) fix K3 DSpark DCP8 MLA head-width and capture-layout defects
- [#2134](https://github.com/ROCm/ATOM/pull/2134) add GLM-5.2 CPP4+DCP4 ATOMesh benchmark coverage

</details>

<details>
<summary>Newly opened: Docs (1)</summary>

- [#2117](https://github.com/ROCm/ATOM/pull/2117) update the GLM5.2 agentic recipe

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (ATOM.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 9b0cdfd4ecc0005095aa558354c5b020e683f6298512ab9201afbb8000983773 -->
