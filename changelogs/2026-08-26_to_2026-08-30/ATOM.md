# ATOM: PR digest (2026-08-26 to 2026-08-30)

_30 merged, 30 newly opened - source ROCm/ATOM, generated 2026-08-30T23:46:04Z_

## TL;DR
- **Model attention:** DeepSeek-V4 and GLM got the most label attention. Merged work enables persistent sparse MLA DCP for GLM-5.2 (`[#2057](https://github.com/ROCm/ATOM/pull/2057)`). Newly opened work covers GLM-5.3-Flash (`[#2051](https://github.com/ROCm/ATOM/pull/2051)`, `[#2061](https://github.com/ROCm/ATOM/pull/2061)`), Qwen3.8 Flash Next (`[#2048](https://github.com/ROCm/ATOM/pull/2048)`, `[#2067](https://github.com/ROCm/ATOM/pull/2067)`), Kimi-K3 LMCache offload (`[#2053](https://github.com/ROCm/ATOM/pull/2053)`) and a DeepSeek-V4-Flash MI308X recipe (`[#2086](https://github.com/ROCm/ATOM/pull/2086)`).
- **Biggest performance work:** Decode Context Parallel (DCP) for MLA/DSA. Merged: fused indexer small ops (`[#2055](https://github.com/ROCm/ATOM/pull/2055)`), fused `indexer_qk_rope_quant_and_cache` (`[#2070](https://github.com/ROCm/ATOM/pull/2070)`) and speculative decoding under DCP (`[#2033](https://github.com/ROCm/ATOM/pull/2033)`). Open: fused DCP top-k merge (`[#2087](https://github.com/ROCm/ATOM/pull/2087)`) and a DCP KV-transfer megaPR (`[#2054](https://github.com/ROCm/ATOM/pull/2054)`).
- **Spec-decode and state:** Draft forwards are now warmed at target-captured batch sizes (`[#2042](https://github.com/ROCm/ATOM/pull/2042)`). SSM replay landed for GDN attention and KDA (`[#1883](https://github.com/ROCm/ATOM/pull/1883)`), and a paged state cache landed (`[#2045](https://github.com/ROCm/ATOM/pull/2045)`).
- **Kernels and MoE:** Open work includes Gluon MoE for TP and EP (`[#2046](https://github.com/ROCm/ATOM/pull/2046)`, `[#2047](https://github.com/ROCm/ATOM/pull/2047)`), fused activation plus FP8 per-token quant for Kimi (`[#2089](https://github.com/ROCm/ATOM/pull/2089)`, `[#2080](https://github.com/ROCm/ATOM/pull/2080)`), and a DP-sharded LM head (`[#2076](https://github.com/ROCm/ATOM/pull/2076)`, merged).
- **Direction:** Long-context DCP/PCP serving, new model bring-up on MI355X/gfx1250, and correctness hardening around spec-decode, scheduling and cudagraph.

## Most important PRs
**[#2045](https://github.com/ROCm/ATOM/pull/2045) paged state cache**
Adds a paged cache for recurrent/SSM-style state, with changes across attention, MLA and distributed code. It is the base for state checkpointing (`[#2024](https://github.com/ROCm/ATOM/pull/2024)`, open) and for hybrid linear-attention models.

**[#2042](https://github.com/ROCm/ATOM/pull/2042) perf(spec-decode): warm every draft forward at a batch the target captured**
Draft-model forwards are warmed at batch sizes the target already captured. This avoids cold-graph and compile stalls on the draft path and touches the aiter and Triton backends and quantization.

**[#1883](https://github.com/ROCm/ATOM/pull/1883) Enable SSM replay for GDN attention and KDA**
Lets speculative decoding replay SSM state for gated-delta-net and KDA linear-attention layers. Rejected draft tokens can then be handled without recomputation, which makes spec-decode viable on these hybrid architectures.

**[#2057](https://github.com/ROCm/ATOM/pull/2057) Persistent sparse MLA DCP for GLM-5.2**
Turns on the aiter persistent sparse-MLA kernel under DCP for GLM-5.2. This improves long-context decode throughput.

**[#1836](https://github.com/ROCm/ATOM/pull/1836) Diffusion subsystem and MiniMax-H3 video+audio generation**
Adds a diffusion subsystem to ATOM, the largest merged feature by size (+11.4k lines). It extends the engine beyond LLM decoding.

## More changes by area

<details>
<summary>Performance (4)</summary>

- [#2016](https://github.com/ROCm/ATOM/pull/2016) session-aware routing and post-prefill decode protection for DPA
- [#2020](https://github.com/ROCm/ATOM/pull/2020) `merge_chunk` no longer rebuilds the whole backlog on each merge
- [#2050](https://github.com/ROCm/ATOM/pull/2050) (open) reduces memory pressure from initializing multiple comm groups
- [#2039](https://github.com/ROCm/ATOM/pull/2039) (open) syncs DPA forward metadata over the device group

</details>

<details>
<summary>Kernels & attention (9)</summary>

- [#2026](https://github.com/ROCm/ATOM/pull/2026) piecewise core reconstruction, with only the attention compressor piecewise
- [#2069](https://github.com/ROCm/ATOM/pull/2069) fully fuses LM-head argmax packing in Triton
- [#2058](https://github.com/ROCm/ATOM/pull/2058) `QKNormRopeOut` produces its own custom-op return (V4)
- [#2078](https://github.com/ROCm/ATOM/pull/2078) (open) replaces radix_topk with flydsl topk
- [#2077](https://github.com/ROCm/ATOM/pull/2077) (open) DSV4 bf16 opus attention on gfx1250
- [#2087](https://github.com/ROCm/ATOM/pull/2087) (open) opt-in fused DCP decode top-k merge
- [#2060](https://github.com/ROCm/ATOM/pull/2060) (open) DCP decode on the gathered head width; fixes K3's missing QREP q_proj override
- [#2037](https://github.com/ROCm/ATOM/pull/2037) (open) V4 mixed-schedule large-concurrency optimization
- [#2024](https://github.com/ROCm/ATOM/pull/2024) (open) state checkpoint superblock

</details>

<details>
<summary>MoE & quantization (7)</summary>

- [#2047](https://github.com/ROCm/ATOM/pull/2047) (open) Gluon MoE EP
- [#2046](https://github.com/ROCm/ATOM/pull/2046) (open) Gluon MoE TP
- [#2089](https://github.com/ROCm/ATOM/pull/2089) (open) fused activation + FP8 per-token quant for K3 dense/shared MLP and full attention
- [#2080](https://github.com/ROCm/ATOM/pull/2080) (open) fuses SiTUv2 activation with per-token FP8 quant in KimiMLP
- [#2027](https://github.com/ROCm/ATOM/pull/2027) (open) SwiGLU for the Triton MoE dense shared expert on GFX1250 (MiniMax-M3)
- [#2028](https://github.com/ROCm/ATOM/pull/2028) (open) Lumen-RL FP8 rollout weight sync and CUDA Graph stability
- [#2010](https://github.com/ROCm/ATOM/pull/2010) fake-eplb routes on a zero router correction bias

</details>

<details>
<summary>Model support (8)</summary>

- [#2051](https://github.com/ROCm/ATOM/pull/2051) (open) GLM-5.3-Flash (glm5_next) text path on MI355X
- [#2061](https://github.com/ROCm/ATOM/pull/2061) (open) GLM-5.3 Flash support
- [#2048](https://github.com/ROCm/ATOM/pull/2048) (open) Qwen3.8 Flash Next
- [#2067](https://github.com/ROCm/ATOM/pull/2067) (open) Qwen3.8 in the sgl-atom plugin
- [#2053](https://github.com/ROCm/ATOM/pull/2053) (open) LMCache offload for Kimi-K3
- [#2043](https://github.com/ROCm/ATOM/pull/2043) (open) MiniMax-M3 serving conforming to the OpenAI API
- [#2086](https://github.com/ROCm/ATOM/pull/2086) (open) DeepSeek-V4-Flash-0731 MI308X TP4 recipe (draft)
- [#2085](https://github.com/ROCm/ATOM/pull/2085) (open) upgrades the vLLM OOT plugin to 0.28.0

</details>

<details>
<summary>Parallelism & scheduling (5)</summary>

- [#2033](https://github.com/ROCm/ATOM/pull/2033) DSpark speculative decoding under DCP
- [#2076](https://github.com/ROCm/ATOM/pull/2076) DP-sharded LM head with all-to-all logits exchange
- [#2054](https://github.com/ROCm/ATOM/pull/2054) (open) DCP KV transfer (very large)
- [#2049](https://github.com/ROCm/ATOM/pull/2049) (open) fixes DSV4 PCP with MTP
- [#2066](https://github.com/ROCm/ATOM/pull/2066) (open) fixes low MTP acceptance rate for GLM-5.2

</details>

<details>
<summary>Bugfixes (14)</summary>

- [#2088](https://github.com/ROCm/ATOM/pull/2088) settles a step's shape once and fixes the three defects that exposed
- [#1985](https://github.com/ROCm/ATOM/pull/1985) Qwen3.5 block-FP8 correctness under vLLM FULL cudagraph
- [#1994](https://github.com/ROCm/ATOM/pull/1994) PD prefix cache for DCP
- [#2012](https://github.com/ROCm/ATOM/pull/2012) truncates speculative batches at max_tokens
- [#2041](https://github.com/ROCm/ATOM/pull/2041) a rejected request now reaches the waiting client
- [#2006](https://github.com/ROCm/ATOM/pull/2006) accounts for dp_size when preparing the topk buffer in DPA TP-MoE
- [#2073](https://github.com/ROCm/ATOM/pull/2073) sizes fake-eplb router logits to the routed expert count
- [#2040](https://github.com/ROCm/ATOM/pull/2040) scheduler admission counted KV blocks globally against a per-rank pool
- [#2036](https://github.com/ROCm/ATOM/pull/2036) forwards DCP indexer buffers through the rtpllm sparse attn bridge
- [#2072](https://github.com/ROCm/ATOM/pull/2072) replaces `_dcp_num_blocks` with `num_pool_blocks`
- [#2044](https://github.com/ROCm/ATOM/pull/2044) (open) marks the DP lockstep dummy batch as a dummy run
- [#2083](https://github.com/ROCm/ATOM/pull/2083) (open) vllm-atom CI startup failures
- [#2070](https://github.com/ROCm/ATOM/pull/2070) enables fused `indexer_qk_rope_quant_and_cache` for DCP
- [#2055](https://github.com/ROCm/ATOM/pull/2055) fuses DCP indexer small ops and fixes the non-persistent path

</details>

<details>
<summary>CI & build (7)</summary>

- [#2038](https://github.com/ROCm/ATOM/pull/2038) plugin accuracy jobs submitted through Slurm
- [#2056](https://github.com/ROCm/ATOM/pull/2056) Atomesh: two figures for p90 e2e-normalized and ITL interactivity
- [#2068](https://github.com/ROCm/ATOM/pull/2068) updates the aiperf docker image and recipe
- [#2084](https://github.com/ROCm/ATOM/pull/2084) prunes stale Docker data on TW runners
- [#2071](https://github.com/ROCm/ATOM/pull/2071) (open) weekly agentic benchmark CI
- [#2074](https://github.com/ROCm/ATOM/pull/2074) (open) DO NOT MERGE: fixed-length prompts, no warmup bench
- [#2052](https://github.com/ROCm/ATOM/pull/2052) clarifies no-tools parser behavior and improves docs

</details>

<details>
<summary>Docs (1)</summary>

- [#2059](https://github.com/ROCm/ATOM/pull/2059) (open) fixes a duplicated table on the atom overview

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (ATOM.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 723d23d6804e27117c5525eab8bcc5cfb74743595375a11e3496f9c952bcf8db -->
