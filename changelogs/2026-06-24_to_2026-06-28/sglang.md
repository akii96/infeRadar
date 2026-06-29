# sglang: PR digest (2026-06-24 to 2026-06-28)

_207 merged, 250 newly opened - source sgl-project/sglang, generated 2026-06-28T22:21:54Z_

## TL;DR
- **DeepSeek & GLM** dominated model support: DeepSeek saw major in-progress work on V4 CP KV LayerSplit and DSpark speculative decoding, plus merged V3/V4 MoE and FP8 KV fixes. GLM-5 received fused DSA indexer Q/K paths, JIT fused A GEMM, and extensive GLM-5.2 NVFP4 tuning.
- **MiniMax-M3** got significant attention with merged HiCache/sparse KV pool support and massive in-progress PRs for Wint4Abf16/Win4Afp8 quantization on Hopper.
- **Performance & Kernels**: Major needle-moving work includes newly opened PRs for FlashInfer Cascade Attention (cross-request shared-prefix decode), DeepEPv2 MoE A2A backend, and NVFP4 KV cache for SM120/SM121.
- **Speculative Decoding & Architecture**: Merged foundational work for decoupled speculative decoding via IPC protocol, and in-progress work on DFlash/DSpark speculative decoding.
- **Multimodal & Diffusion**: Added support for JoyEcho multi-shot A/V generation and Krea 2, alongside in-progress Triton/FA2 NVFP4 KV cache migrations for DiffusionGemma.

## Most important PRs
- **[#29107](https://github.com/sgl-project/sglang/pull/29107)** Adds MiniMax-M3 Wint4Abf16 and Win4Afp8 support on Hopper, introducing extensive Triton and Cutlass kernels for mixed-precision MoE.
- **[#29304](https://github.com/sgl-project/sglang/pull/29304)** Implements NVFP4 KV cache for SM120/SM121, enabling Gemma-4 VO-split and FP4 prefix-cache correctness via FlashInfer.
- **[#29288](https://github.com/sgl-project/sglang/pull/29288)** Introduces FlashInfer's Cascade Attention Backend, enabling highly efficient cross-request shared-prefix decoding.
- **[#29525](https://github.com/sgl-project/sglang/pull/29525)** Adds the DeepEPv2 (ElasticBuffer) MoE all-to-all backend, optimizing distributed MoE routing and quantization on NVIDIA hardware.
- **[#14194](https://github.com/sgl-project/sglang/pull/14194)** Implements decode context parallel (DCP) for DeepSeek-V2, integrating FlashInfer and Triton attention backends with MLA and scheduler updates.

## More changes by area

<details>
<summary>Performance (10)</summary>

- [#29117](https://github.com/sgl-project/sglang/pull/29117) optimize GDN prefill performance on CPU
- [#27053](https://github.com/sgl-project/sglang/pull/27053) BCG support and prefill enhancements for GLM5
- [#29223](https://github.com/sgl-project/sglang/pull/29223) shard Kimi-K2.5 Eagle3 draft fc + symm-mem AG
- [#29103](https://github.com/sgl-project/sglang/pull/29103) reduce scatter decode for AMD dsv4 aiter
- [#29147](https://github.com/sgl-project/sglang/pull/29147) shard Qwen Text Embed in SP for diffusion
- [#29075](https://github.com/sgl-project/sglang/pull/29075) overlap result D2H copy with the next forward step
- [#29513](https://github.com/sgl-project/sglang/pull/29513) add Sana-WM Triton optimizations
- [#29164](https://github.com/sgl-project/sglang/pull/29164) route slow tokenizers through `.encode()` on dynamic batch path
- [#29306](https://github.com/sgl-project/sglang/pull/29306) enable compile warmup for diffusion decode
- [#29202](https://github.com/sgl-project/sglang/pull/29202) enable draft-extend CUDA graph and reduce bubble for MTP on AMD

</details>

<details>
<summary>Kernels & attention (20)</summary>

- [#28451](https://github.com/sgl-project/sglang/pull/28451) add ReplaySSM buffered output-only decode for Linear Attention
- [#27397](https://github.com/sgl-project/sglang/pull/27397) support JIT fused A GEMM (MLA down projection) and GLM-5 hidden size
- [#27705](https://github.com/sgl-project/sglang/pull/27705) fuse the DSA (V3.2, GLM-5.x) indexer Q/K paths into single kernels
- [#29498](https://github.com/sgl-project/sglang/pull/29498) optimize DSA CUDA graph replay metadata generation
- [#28320](https://github.com/sgl-project/sglang/pull/28320) add fused QK GemmaRMSNorm + RoPE + gate kernel for Qwen3.5
- [#28975](https://github.com/sgl-project/sglang/pull/28975) add opt-in Triton fp8 sparse-MLA prefill kernel for AMD GLM5
- [#28624](https://github.com/sgl-project/sglang/pull/28624) optimize LTX2.3 CFG/SP paths
- [#28757](https://github.com/sgl-project/sglang/pull/28757) skip redundant -inf pre-fill of HIP indexer MQA-logits for AMD GLM5
- [#29267](https://github.com/sgl-project/sglang/pull/29267) add indices in chunk_gated_delta_rule for CPU
- [#29415](https://github.com/sgl-project/sglang/pull/29415) remove host H2D sync in `_apply_cuda_graph_metadata` for DSA
- [#29423](https://github.com/sgl-project/sglang/pull/29423) avoid dynamic Q quantization in trtllm_mha
- [#29383](https://github.com/sgl-project/sglang/pull/29383) add InfLLM v2 attention kernels
- [#29533](https://github.com/sgl-project/sglang/pull/29533) add page-major KV/state layout
- [#29297](https://github.com/sgl-project/sglang/pull/29297) add training-free sparse attention indexer for GLM4-MoE decode
- [#29132](https://github.com/sgl-project/sglang/pull/29132) add `[v,k]` state layout option via `linear_backend="seg_la_vk"`
- [#29451](https://github.com/sgl-project/sglang/pull/29451) integrate FlashInfer for MTP cache mode at final recovery stage
- [#29362](https://github.com/sgl-project/sglang/pull/29362) add dsv4 ep tbo prefill
- [#29315](https://github.com/sgl-project/sglang/pull/29315) add LTX2 TE NVFP4 FFN fast path
- [#29472](https://github.com/sgl-project/sglang/pull/29472) add FlashKDA prefill backend for safe-gate KDA linear attention
- [#29343](https://github.com/sgl-project/sglang/pull/29343) build page table on-device and drop seq_lens_cpu D2H sync for FA3

</details>

<details>
<summary>MoE & quantization (12)</summary>

- [#28082](https://github.com/sgl-project/sglang/pull/28082) add ULP-based quant error tolerance via `allow_quant_error`
- [#28928](https://github.com/sgl-project/sglang/pull/28928) add Qwen-Image ModelOpt NVFP4 support
- [#27939](https://github.com/sgl-project/sglang/pull/27939) support online MXFP8 quantization for ungated MoE
- [#29142](https://github.com/sgl-project/sglang/pull/29142) run routed experts on main stream in dual-stream MoE for DeepSeek V3
- [#29452](https://github.com/sgl-project/sglang/pull/29452) revert running routed experts on main stream in dual-stream MoE
- [#29462](https://github.com/sgl-project/sglang/pull/29462) skip FlashInfer FP8 autotune for MXFP8 quantized models
- [#29328](https://github.com/sgl-project/sglang/pull/29328) add NVFP4 to MXFP4 online requantization on AMD GPUs
- [#29402](https://github.com/sgl-project/sglang/pull/29402) add DeepEP v2 MoE dispatcher
- [#29190](https://github.com/sgl-project/sglang/pull/29190) add MoE NVFP4 kernel of B12X for SM120
- [#29386](https://github.com/sgl-project/sglang/pull/29386) add FlashInfer W4AFP8 MoE path
- [#29112](https://github.com/sgl-project/sglang/pull/29112) support mixed precision models combining mxfp8 linears with nvfp4 experts
- [#29468](https://github.com/sgl-project/sglang/pull/29468) map inactive virtual-expert tokens to no-LoRA

</details>

<details>
<summary>Model support (11)</summary>

- [#27420](https://github.com/sgl-project/sglang/pull/27420) add JoyEcho multi-shot A/V generation support for Diffusion
- [#29186](https://github.com/sgl-project/sglang/pull/29186) add Baidu Unlimited-OCR support
- [#29052](https://github.com/sgl-project/sglang/pull/29052) add Krea 2 support for Diffusion
- [#28952](https://github.com/sgl-project/sglang/pull/28952) add DeepSeek V4 Flash demo notebook
- [#28940](https://github.com/sgl-project/sglang/pull/28940) add Qwen3-VL / Moss-VL ViT preprocessing optimizations
- [#29194](https://github.com/sgl-project/sglang/pull/29194) add GLM-5.1 MXFP4 (MI355X) and enable EAGLE for gfx950
- [#29253](https://github.com/sgl-project/sglang/pull/29253) add MiMo V2.5 Blackwell vision FA4 recipe
- [#29189](https://github.com/sgl-project/sglang/pull/29189) add Gigachat 3.5 support
- [#29226](https://github.com/sgl-project/sglang/pull/29226) add Command A+ cookbook
- [#29580](https://github.com/sgl-project/sglang/pull/29580) support GLM DSA serving on RTX PRO 6000 (SM120)
- [#29404](https://github.com/sgl-project/sglang/pull/29404) add DeepReinforce Ornith-1.0 to cookbook

</details>

<details>
<summary>Parallelism & scheduling (25)</summary>

- [#28713](https://github.com/sgl-project/sglang/pull/28713) add mem-cache / HiCache / sparse KV pool for minimax-m3
- [#27563](https://github.com/sgl-project/sglang/pull/27563) support NIXL DRAM KV destinations for HiSparse
- [#25090](https://github.com/sgl-project/sglang/pull/25090) support triton backend decode context parallel for Qwen3.5 on AMD
- [#27634](https://github.com/sgl-project/sglang/pull/27634) add decoupled speculative decoding IPC protocol and cross-process request id
- [#28258](https://github.com/sgl-project/sglang/pull/28258) add NIXL FILE cache cleaner for HiCache
- [#26245](https://github.com/sgl-project/sglang/pull/26245) support DP-aware PD router dispatch
- [#29089](https://github.com/sgl-project/sglang/pull/29089) extract DFlash prefill refill into a standalone MinFreeSlotsDelayer
- [#28714](https://github.com/sgl-project/sglang/pull/28714) add disagg K-only index-K transfer for minimax-m3
- [#28614](https://github.com/sgl-project/sglang/pull/28614) remove large host mem constraint for HiCache
- [#29395](https://github.com/sgl-project/sglang/pull/29395) capture DFLASH draft greedy sampling inside the draft decode cuda graph
- [#29556](https://github.com/sgl-project/sglang/pull/29556) drop verify_done barrier for dflash and rely on scheduler WAR fallback
- [#29316](https://github.com/sgl-project/sglang/pull/29316) early-send cached-prefix KV overlapping uncached prefill forward for PD
- [#29122](https://github.com/sgl-project/sglang/pull/29122) make the overlap bonus-token relay unconditional for Spec
- [#29187](https://github.com/sgl-project/sglang/pull/29187) add DeepSeek V4 CP KV LayerSplit
- [#29173](https://github.com/sgl-project/sglang/pull/29173) add reference-aware Radix Cache for agentic multi-turn workloads
- [#29475](https://github.com/sgl-project/sglang/pull/29475) add priority-based worker eligibility gating for router
- [#29538](https://github.com/sgl-project/sglang/pull/29538) add DSpark speculative decoding for DeepSeek-V4
- [#29421](https://github.com/sgl-project/sglang/pull/29421) add DSA Cache Layer Split under Prefill CP for GLM5.2
- [#29168](https://github.com/sgl-project/sglang/pull/29168) enable unified-KV HiSparse on ROCm for DeepSeek-V4
- [#29191](https://github.com/sgl-project/sglang/pull/29191) support hybrid models in nixl hicache backend
- [#29574](https://github.com/sgl-project/sglang/pull/29574) reproduce LMetric Multiplication Scheduling in SGLang Gateway
- [#29185](https://github.com/sgl-project/sglang/pull/29185) support decode context parallel for DeepSeek V4 with unified kv attention backend on AMD
- [#29353](https://github.com/sgl-project/sglang/pull/29353) add transactional-rollback for scheduler
- [#29199](https://github.com/sgl-project/sglang/pull/29199) add experimental agent-aware KV cache hints
- [#29369](https://github.com/sgl-project/sglang/pull/29369) clean up full KV for SWA tombstone leaves

</details>

<details>
<summary>Hardware & arch (10)</summary>

- [#18139](https://github.com/sgl-project/sglang/pull/18139) add Intel Quantization Support in SGLang
- [#27833](https://github.com/sgl-project/sglang/pull/27833) enable BCG on ROCm and route aiter prefill via MHA for Kimi-2.5
- [#26724](https://github.com/sgl-project/sglang/pull/26724) adapt to support operator FA3 in deterministic inference on NPU
- [#27870](https://github.com/sgl-project/sglang/pull/27870) add XPU support for set_embed_and_head and fused QK RMSNorm kernel
- [#27783](https://github.com/sgl-project/sglang/pull/27783) support hc_split_sinkhorn on XPU using sgl_kernel for DeepSeek V4
- [#28872](https://github.com/sgl-project/sglang/pull/28872) adapt fused rope qk mqa optimize for NPU
- [#29490](https://github.com/sgl-project/sglang/pull/29490) add minimal Apple Silicon server startup for hybrid GDN models on MLX
- [#29192](https://github.com/sgl-project/sglang/pull/29192) enable GLM on Xeon
- [#29433](https://github.com/sgl-project/sglang/pull/29433) enable pinned memory and fuse shared output to optimize LLaDA2 on NPU
- [#29509](https://github.com/sgl-project/sglang/pull/29509) optimize GLM-4.7-Flash with fused kernels on NPU

</details>

<details>
<summary>API & serving (12)</summary>

- [#29342](https://github.com/sgl-project/sglang/pull/29342) add native Exa-backed web_search support
- [#22659](https://github.com/sgl-project/sglang/pull/22659) add sleep/wake support for diffusion engine
- [#29467](https://github.com/sgl-project/sglang/pull/29467) count requests/responses at the HTTP edge for true intake
- [#29436](https://github.com/sgl-project/sglang/pull/29436) add first-class session identity in SGLang
- [#29535](https://github.com/sgl-project/sglang/pull/29535) add scheduler metrics reporter init hook
- [#29207](https://github.com/sgl-project/sglang/pull/29207) add scheduler metrics extension hooks
- [#29104](https://github.com/sgl-project/sglang/pull/29104) add opt-in request-count admission control / backpressure for router
- [#29116](https://github.com/sgl-project/sglang/pull/29116) forward cleartext h2c to `--enable-http2` engines
- [#29242](https://github.com/sgl-project/sglang/pull/29242) fix Responses API and Anthropic `/v1/messages` thinking block signature
- [#29325](https://github.com/sgl-project/sglang/pull/29325) add Responses support
- [#29165](https://github.com/sgl-project/sglang/pull/29165) add in-flight request cap (`max_inflight_requests`) to sgl-model-gateway
- [#29474](https://github.com/sgl-project/sglang/pull/29474) add `/v1/messages` Anthropic passthrough route

</details>

<details>
<summary>Refactors (10)</summary>

- [#28001](https://github.com/sgl-project/sglang/pull/28001) refactor weight processing in RL weight update
- [#28492](https://github.com/sgl-project/sglang/pull/28492) simplify `MultiLayerEagleDraftExtendCudaGraphRunner` to use rotation
- [#28688](https://github.com/sgl-project/sglang/pull/28688) convert IPC dataclasses to msgspec.Struct with opt-in msgpack transport
- [#28211](https://github.com/sgl-project/sglang/pull/28211) centralize FlashInfer CUTLASS MoE runner
- [#29214](https://github.com/sgl-project/sglang/pull/29214) rename IPC structs, improve typing, and remove SenderWrapper
- [#21531](https://github.com/sgl-project/sglang/pull/21531) migrate dsv3_router_gemm from AOT sgl-kernel to JIT kernel
- [#29224](https://github.com/sgl-project/sglang/pull/29224) extract style and type annotation improvements from [#28688](https://github.com/sgl-project/sglang/pull/28688)
- [#29220](https://github.com/sgl-project/sglang/pull/29220) dissolve `EagleDraftInputV2Mixin` so spec-info dataclasses hold data only
- [#29228](https://github.com/sgl-project/sglang/pull/29228) merge dflash triton kernels into a single `dflash.py`
- [#29365](https://github.com/sgl-project/sglang/pull/29365) consolidate decode-context-parallel (DCP) helpers under `layers/cp/dcp/`

</details>

<details>
<summary>Bugfixes (10)</summary>

- [#29182](https://github.com/sgl-project/sglang/pull/29182) fix garbage output of Minimax-M3-mxfp4 on AMD
- [#28953](https://github.com/sgl-project/sglang/pull/28953) fix EP cuda-graph crash for experimental_sgl_trtllm MoE-LoRA
- [#25071](https://github.com/sgl-project/sglang/pull/25071) fix normal text detection before tool call in kimik2_detector
- [#28662](https://github.com/sgl-project/sglang/pull/28662) requantize weight scales to UE8M0 for DeepGEMM on Blackwell
- [#29464](https://github.com/sgl-project/sglang/pull/29464) fix EAGLE draft hidden dim extraction and centralize spec helpers
- [#28906](https://github.com/sgl-project/sglang/pull/28906) detect-and-passthrough mid-conversation system messages for Anthropic
- [#29520](https://github.com/sgl-project/sglang/pull/29520) fix prefill-aware SWA floor tracking
- [#29250](https://github.com/sgl-project/sglang/pull/29250) fix MiniMax MSA fallback when fmha plan is unavailable
- [#28237](https://github.com/sgl-project/sglang/pull/28237) correct fused shared-expert scaling on aiter/DeepEP path
- plus 60 more minor bugfixes

</details>

<details>
<summary>Tests, CI & Docs (10)</summary>

- [#27433](https://github.com/sgl-project/sglang/pull/27433) refactor and enhance NPU Nightly CI
- [#28762](https://github.com/sgl-project/sglang/pull/28762) refactor Diffusion CI
- [#29084](https://github.com/sgl-project/sglang/pull/29084) add MI355X disaggregation nightly benchmark
- [#28103](https://github.com/sgl-project/sglang/pull/28103) add DeepSeek V4 Pro GB300 nightly and expand Kimi K25 nightly test
- [#28623](https://github.com/sgl-project/sglang/pull/28623) reduce CPU CI scope with base-c suite
- [#29447](https://github.com/sgl-project/sglang/pull/29447) add per-stage NVIDIA model inventory tool
- [#29125](https://github.com/sgl-project/sglang/pull/29125) debug MI355X 1P1D disaggregation nightly
- [#29403](https://github.com/sgl-project/sglang/pull/29403) sync NPU nightly test improvements from Ascend testcases
- [#29492](https://github.com/sgl-project/sglang/pull/29492) update NPU best practice docs from testcases
- plus 45 more minor test, CI, and doc updates

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (sglang.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
