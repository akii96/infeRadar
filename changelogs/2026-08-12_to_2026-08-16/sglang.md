# sglang: PR digest (2026-08-12 to 2026-08-16)

_239 merged, 334 newly opened - source sgl-project/sglang, generated 2026-08-16T21:52:16Z_

## TL;DR
*   **MiniMax & DeepSeek-V4 dominated:** Extensive work landed for MiniMax (M3/H3) and DeepSeek-V4, including NPU w8a8 adaptation, sparse attention paths, and native VAE/AdaLN support. Qwen 3.8 and Kimi-K3 also saw major feature additions.
*   **Aggressive low-bit quantization:** Massive expansion of MXFP4 and NVFP4 support across AMD, NPU, and NVIDIA (SM90/SM120) backends, including online requantization and FlashInfer/CUTLASS MoE integrations.
*   **Multimodal & Diffusion explosion:** Native support added for Hunyuan3D, LTX-2.5, Qwen2.5-VL, SANA-Video, and Cosmos3, with newly opened work for SenseNova U1 and MAGI-2-preview.
*   **Architectural unification:** Significant in-progress refactors aim to unify memory read-paths across attention backends, deprecate legacy prefill CP, and introduce a dedicated LoRA MoE execution engine.
*   **Overall direction:** The engine is rapidly maturing its support for next-gen hardware (SM12x, MI35x) and extreme low-bit MoE inference, while heavily optimizing distributed prompt decoding and multimodal caching.

## Most important PRs
*   **[#32991](https://github.com/sgl-project/sglang/pull/32991)** Adds architecture-owned SM12x FlashAttention-4 kernels, laying the groundwork for next-generation NVIDIA hardware performance.
*   **[#34803](https://github.com/sgl-project/sglang/pull/34803)** (Opened) Introduces a dedicated `sgl_lora` MoE execution engine with JSON config resolution, massively expanding PEFT capabilities for MoE architectures.
*   **[#34613](https://github.com/sgl-project/sglang/pull/34613)** (Opened) Unifies the memory read-path ID space into a single choke point, enabling seamless integration across FA3, FlashInfer, TRT-LLM MHA, and FlashMLA.
*   **[#32017](https://github.com/sgl-project/sglang/pull/32017)** Overlaps model checkpoint staging with CUDA graph capture, significantly reducing startup latency for large models.
*   **[#34905](https://github.com/sgl-project/sglang/pull/34905)** (Opened) Implements layer-wise KV transfer for prompt-decoding (PD) disaggregation, optimizing distributed inference across AMD and NVIDIA clusters.

## More changes by area

<details>
<summary>Model support (31)</summary>

- [#34871](https://github.com/sgl-project/sglang/pull/34871) GLM 5.2 optimization sync
- [#34585](https://github.com/sgl-project/sglang/pull/34585) (Opened) Support Qwen 3.8
- [#34980](https://github.com/sgl-project/sglang/pull/34980) Native Hunyuan3D Paint and Delight models
- [#34471](https://github.com/sgl-project/sglang/pull/34471) Support LTX-2.5
- [#34404](https://github.com/sgl-project/sglang/pull/34404) Cache Kimi-K3 per-image processor artifacts
- [#23274](https://github.com/sgl-project/sglang/pull/23274) Support LongCat-Image
- [#33465](https://github.com/sgl-project/sglang/pull/33465) Support Kimi-K3 on NPU
- [#31590](https://github.com/sgl-project/sglang/pull/31590) Add Cosmos3 Edge and Distilled checkpoints support
- [#34896](https://github.com/sgl-project/sglang/pull/34896) Use native Qwen2.5-VL generation
- [#32921](https://github.com/sgl-project/sglang/pull/32921) Add native SANA-Video T2V support
- [#34650](https://github.com/sgl-project/sglang/pull/34650) Rebuild MiniMax-H3 AdaLN outputs on demand
- [#34945](https://github.com/sgl-project/sglang/pull/34945) Native Qwen3-VL vision encoder
- [#34949](https://github.com/sgl-project/sglang/pull/34949) Route MiniMax H3 VAE attention through native backends
- [#34951](https://github.com/sgl-project/sglang/pull/34951) Native ERNIE prompt enhancer
- [#34359](https://github.com/sgl-project/sglang/pull/34359) Support native and PEFT MiniMax H3 LoRAs
- plus 16 more minor model support updates
</details>

<details>
<summary>Kernels & attention (48)</summary>

- [#33997](https://github.com/sgl-project/sglang/pull/33997) Bump FlashInfer to 0.6.17 and remove Kimi K3 workarounds
- [#32593](https://github.com/sgl-project/sglang/pull/32593) Enable Helion backend for Kimi Delta-Attention
- [#34274](https://github.com/sgl-project/sglang/pull/34274) Content-addressed JIT build cache
- [#34509](https://github.com/sgl-project/sglang/pull/34509) Migrate moe_topk_softmax from AOT to JIT
- [#25855](https://github.com/sgl-project/sglang/pull/25855) Optimize paged_mqa_metadata for DeepSeek-V4
- [#34617](https://github.com/sgl-project/sglang/pull/34617) Fuse eager QKV packing and high-quality QKNorm for HunyuanVideo
- [#34275](https://github.com/sgl-project/sglang/pull/34275) Fuse Cosmos3 QK norm, RoPE, and KV packing
- [#31574](https://github.com/sgl-project/sglang/pull/31574) Batch embedding cache host-device range copies
- [#34620](https://github.com/sgl-project/sglang/pull/34620) Fuse QKNorm with full-width RoPE for ERNIE
- [#34616](https://github.com/sgl-project/sglang/pull/34616) Fuse eager AdaLN and packed SwiGLU for FLUX.2
- [#34928](https://github.com/sgl-project/sglang/pull/34928) Accelerate Sana BCG with bit-exact conv post-processing
- [#33827](https://github.com/sgl-project/sglang/pull/33827) Make Cache-DiT actually cache on MiniMax-H3
- [#34584](https://github.com/sgl-project/sglang/pull/34584) Wan2.2-TI2V: fuse per-token adaLN table add
- [#34314](https://github.com/sgl-project/sglang/pull/34314) Ideogram-4: fuse Qwen3-style RoPE and SwiGLU silu-mul
- [#34932](https://github.com/sgl-project/sglang/pull/34932) Accelerate Cosmos3 T2I QKNorm+RoPE
- plus 33 more minor kernel and attention updates
</details>

<details>
<summary>MoE & quantization (32)</summary>

- [#32941](https://github.com/sgl-project/sglang/pull/32941) Adaptation of Minimax M3(w8a8) for NPU platforms
- [#29328](https://github.com/sgl-project/sglang/pull/29328) NVFP4 to MXFP4 Online Requantization on AMD GPUs
- [#33559](https://github.com/sgl-project/sglang/pull/33559) Add triton moe TMA up support
- [#28666](https://github.com/sgl-project/sglang/pull/28666) Fuse shared_expert_gate GEMV into the MoE append kernel
- [#34331](https://github.com/sgl-project/sglang/pull/34331) Add tuned Triton tile configs for channelwise FP8 GEMM
- [#28354](https://github.com/sgl-project/sglang/pull/28354) Support FlashInfer CuTe DSL NVFP4 MoE quantization
- [#32944](https://github.com/sgl-project/sglang/pull/32944) Fuse swiglu moe up gemm epilogue
- [#29593](https://github.com/sgl-project/sglang/pull/29593) Add amx cpu support for auto-round
- [#31856](https://github.com/sgl-project/sglang/pull/31856) Accelerate AITER unified-attention decode with scaled FP8 Q
- [#30318](https://github.com/sgl-project/sglang/pull/30318) Add mxfp4-w4a8 MOE Quantization Support for NPU
- [#34476](https://github.com/sgl-project/sglang/pull/34476) Add GLM-5.2 MXFP4 wide-EP16 2P1D nightly recipes
- [#34042](https://github.com/sgl-project/sglang/pull/34042) Add flashinfer cute-dsl backend for mxfp8 gemm
- [#33945](https://github.com/sgl-project/sglang/pull/33945) Support deterministic FA4 for GLM-4.7-Flash
- [#34883](https://github.com/sgl-project/sglang/pull/34883) Use explicit SiTU activation for MegaMoE
- [#34150](https://github.com/sgl-project/sglang/pull/34150) Add H200 Triton MoE configs for E256 N512
- plus 17 more minor MoE and quantization updates
</details>

<details>
<summary>Parallelism & scheduling (51)</summary>

- [#34736](https://github.com/sgl-project/sglang/pull/34736) Unify component residency controls
- [#34793](https://github.com/sgl-project/sglang/pull/34793) Flatten L2 transfer execution
- [#30827](https://github.com/sgl-project/sglang/pull/30827) Add cache salt support to KV cache events
- [#34391](https://github.com/sgl-project/sglang/pull/34391) Support dynamic CPU offload components
- [#34534](https://github.com/sgl-project/sglang/pull/34534) Add --dit-layerwise-residency-policy for strided DiT residency
- [#31479](https://github.com/sgl-project/sglang/pull/31479) Coalesce cache events
- [#34607](https://github.com/sgl-project/sglang/pull/34607) Add bit-exact unified radix cache KL test for hybrid SWA + mamba
- [#34284](https://github.com/sgl-project/sglang/pull/34284) Track max prefill batch size over recent real admissions
- [#34763](https://github.com/sgl-project/sglang/pull/34763) Support mamba-radix-cache-strategy extra_buffer_lazy with DFLASH
- [#34615](https://github.com/sgl-project/sglang/pull/34615) Make auto residency decisions component-scoped
- [#34870](https://github.com/sgl-project/sglang/pull/34870) Fix swa eviction frontier for bigram keys
- [#32637](https://github.com/sgl-project/sglang/pull/32637) Optimize delayed sample and mrope position computation
- [#34808](https://github.com/sgl-project/sglang/pull/34808) Fix mamba checkpoint depth under dcp
- [#34729](https://github.com/sgl-project/sglang/pull/34729) Retain SWA down to the last state checkpoint
- [#35030](https://github.com/sgl-project/sglang/pull/35030) Add bit-exact guard for extra_buffer_lazy
- plus 36 more minor parallelism and scheduling updates
</details>

<details>
<summary>Performance (10)</summary>

- [#35016](https://github.com/sgl-project/sglang/pull/35016) Tighten NVIDIA perf baselines
- [#32755](https://github.com/sgl-project/sglang/pull/32755) Occupancy tuning for DSA indexer fp8-quant Q kernel
- [#34614](https://github.com/sgl-project/sglang/pull/34614) Fuse the a2a pack/unpack copies in the MLA LSE reduce
- [#30024](https://github.com/sgl-project/sglang/pull/30024) Default block_quota=16 for MLA page_first KV gather
- [#27689](https://github.com/sgl-project/sglang/pull/27689) FlashInfer MLA: remove blocking D2H in spec-decode plan
- [#29202](https://github.com/sgl-project/sglang/pull/29202) Enable draft-extend CUDA graph and reduce bubble for MTP
- [#33857](https://github.com/sgl-project/sglang/pull/33857) Skip trivial DSV4 nonpaged indexer logits
- [#34759](https://github.com/sgl-project/sglang/pull/34759) Fix EP1 decode performance regression
- [#34775](https://github.com/sgl-project/sglang/pull/34775) (Opened) Batch DSA cache relocation across layers
- [#34528](https://github.com/sgl-project/sglang/pull/34528) (Opened) Add optional FlashInfer PCIe-IPC all-reduce for switch-free hosts
</details>

<details>
<summary>API & serving (16)</summary>

- [#34753](https://github.com/sgl-project/sglang/pull/34753) Add extensible serve backend plugins
- [#33895](https://github.com/sgl-project/sglang/pull/33895) Move the PD bootstrap registry under api_server::disaggregation
- [#34892](https://github.com/sgl-project/sglang/pull/34892) Add safeguards for remote media URLs
- [#34458](https://github.com/sgl-project/sglang/pull/34458) Make DeepSeek-V4 reasoning and tool-call streaming parsing chunk-invariant
- [#33593](https://github.com/sgl-project/sglang/pull/33593) Expose top-p-only sampling masks
- [#34796](https://github.com/sgl-project/sglang/pull/34796) Add --http2-max-concurrent-streams server arg
- [#34141](https://github.com/sgl-project/sglang/pull/34141) Reserve multimodal runtime allocations and keep padded inputs aligned
- [#34533](https://github.com/sgl-project/sglang/pull/34533) (Opened) Add --tokenizer-backend=gigatoken
- [#34488](https://github.com/sgl-project/sglang/pull/34488) (Opened) Add response-level input/output token ids to chat completions
- [#34721](https://github.com/sgl-project/sglang/pull/34721) (Opened) Unify MM feature transport on POSIX shm
- [#34699](https://github.com/sgl-project/sglang/pull/34699) (Opened) Separate input_ids from control plane message
- [#34531](https://github.com/sgl-project/sglang/pull/34531) (Opened) Support `save_remote_model` and `save_sharded_model`
- [#34553](https://github.com/sgl-project/sglang/pull/34553) (Opened) Add --enable-sort-tool-schema-keys
- [#35056](https://github.com/sgl-project/sglang/pull/35056) (Opened) Add hierarchical startup-time breakdown
- [#34879](https://github.com/sgl-project/sglang/pull/34879) (Opened) Rust server custom logit processor
- [#34981](https://github.com/sgl-project/sglang/pull/34981) (Opened) Add a pre-weight-processing model loader hook
</details>

<details>
<summary>Hardware & arch (11)</summary>

- [#34376](https://github.com/sgl-project/sglang/pull/34376) Make the linear-attn kernel choice per-runner
- [#34238](https://github.com/sgl-project/sglang/pull/34238) Broadcast the EAGLE greedy verify decision across TP ranks on ROCm
- [#34597](https://github.com/sgl-project/sglang/pull/34597) Run V4 MTP target-verify through the decode kernel
- [#34837](https://github.com/sgl-project/sglang/pull/34837) Add concat_and_cast_mha_k_pad_kernel to support 12-head
- [#35013](https://github.com/sgl-project/sglang/pull/35013) (Opened) Split packed MTP HiCache transfers by pool
- [#34944](https://github.com/sgl-project/sglang/pull/34944) (Opened) Preserve parity in folded NPU paths
- [#34855](https://github.com/sgl-project/sglang/pull/34855) (Opened) Fix NPU Ring Attention varlen dispatch
- [#34794](https://github.com/sgl-project/sglang/pull/34794) (Opened) Fix NEXTN/MTP conv-window layout corrupting verify output
- [#35043](https://github.com/sgl-project/sglang/pull/35043) (Opened) Enable staged HiCache write-back for DeepSeek V4
- [#34912](https://github.com/sgl-project/sglang/pull/34912) (Opened) Avoid padded Q for unified DSV4 prefill
- [#35040](https://github.com/sgl-project/sglang/pull/35040) (Opened) Use HIP batched copies for HiCache write-back
</details>

<details>
<summary>Bugfixes (67)</summary>

- [#33604](https://github.com/sgl-project/sglang/pull/33604) Fix Whisper transcription for audio over 30 seconds
- [#34464](https://github.com/sgl-project/sglang/pull/34464) Refocus LoRA tests on regression coverage
- [#30762](https://github.com/sgl-project/sglang/pull/30762) Support DeepSeek-V4 hybrid HostPoolGroup
- [#34328](https://github.com/sgl-project/sglang/pull/34328) Fix AMD 2-GPU multimodal-gen partition-count abort
- [#34663](https://github.com/sgl-project/sglang/pull/34663) Refresh docs, retire stale knobs, and fix nightly attribution
- [#34891](https://github.com/sgl-project/sglang/pull/34891) Scope attention backend fallback
- [#34982](https://github.com/sgl-project/sglang/pull/34982) Rename shared-read boundary to shared-read ends and fix wrapper delegation
- [#34121](https://github.com/sgl-project/sglang/pull/34121) Fix cache-first fast path accepting a metadata-only snapshot
- [#34401](https://github.com/sgl-project/sglang/pull/34401) Fix model-driven DiT layerwise offload auto policy
- [#34788](https://github.com/sgl-project/sglang/pull/34788) Restore layer-level DSV4 RoPE policy
- [#34766](https://github.com/sgl-project/sglang/pull/34766) Carry the backend on Kimi-K3 deferred preprocessing configs
- [#33006](https://github.com/sgl-project/sglang/pull/33006) Use FlashInfer fused top-k for packed PAGED rows
- [#34662](https://github.com/sgl-project/sglang/pull/34662) Restore VLM nightly regression coverage
- [#34347](https://github.com/sgl-project/sglang/pull/34347) Fix SM120 QKNorm+RoPE rounding
- [#34575](https://github.com/sgl-project/sglang/pull/34575) Unshard FSDP root group for custom encoder entry points
- plus 52 more minor bugfixes
</details>

<details>
<summary>Tests, CI & build (36)</summary>

- [#34520](https://github.com/sgl-project/sglang/pull/34520) Remove 22 unmaintained benchmarks
- [#34309](https://github.com/sgl-project/sglang/pull/34309) Prune redundant CPU test overhead
- [#34204](https://github.com/sgl-project/sglang/pull/34204) Swap the AMD PR gate to ROCm 7.2
- [#34913](https://github.com/sgl-project/sglang/pull/34913) Move the static ratchets back to CPU unit tests
- [#34477](https://github.com/sgl-project/sglang/pull/34477) Route mmlu and GB300 MMMU-Pro evals through sgl-eval
- plus 31 more minor CI and test updates
</details>

<details>
<summary>Docs (22)</summary>

- [#34379](https://github.com/sgl-project/sglang/pull/34379) GLM 5.2 MXFP4 SGLANG COOKBOOK
- [#34587](https://github.com/sgl-project/sglang/pull/34587) Add Qwen3.8 cookbook
- [#34860](https://github.com/sgl-project/sglang/pull/34860) Add Qwen3.8-27B cookbook page
- [#32414](https://github.com/sgl-project/sglang/pull/32414) Add Reasoning-Aware Compression (RAC) pruning recipe
- [#34809](https://github.com/sgl-project/sglang/pull/34809) Add DeepSeek-V4-Pro-0813 serving recipes
- plus 17 more minor documentation updates
</details>

<details>
<summary>Refactors (5)</summary>

- [#33894](https://github.com/sgl-project/sglang/pull/33894) refactor error responses into shared utils::response helpers
- [#34916](https://github.com/sgl-project/sglang/pull/34916) Rename the WAR read-done fastpath to shared-read-done
- [#34660](https://github.com/sgl-project/sglang/pull/34660) (Opened) refactor mm code for rust tokenizer manager
- [#34529](https://github.com/sgl-project/sglang/pull/34529) (Opened) keep MiniMax-H3's checkpoint QKV row order instead of rewriting it
- [#34926](https://github.com/sgl-project/sglang/pull/34926) (Opened) Clean deprecated DeepSeek V4 Environs
</details>

<details>
<summary>Other (41)</summary>

- [#34267](https://github.com/sgl-project/sglang/pull/34267) config: pin the supplied-instance surface
- [#34264](https://github.com/sgl-project/sglang/pull/34264) config: decisions keyed on the attention backend read the configured pair
- [#34266](https://github.com/sgl-project/sglang/pull/34266) config: the alias form of the runner-side instance read
- [#34263](https://github.com/sgl-project/sglang/pull/34263) config: the last runner-side instance reads read the bags
- [#34269](https://github.com/sgl-project/sglang/pull/34269) config: state the bag contract as what resolution produced
- [#34265](https://github.com/sgl-project/sglang/pull/34265) config: a named entry point for the resolution pipeline
- [#34819](https://github.com/sgl-project/sglang/pull/34819) config: the post-publish consumers of the supplied-instance surface read the bags
- [#34730](https://github.com/sgl-project/sglang/pull/34730) Organize environment variable registry
- [#34642](https://github.com/sgl-project/sglang/pull/34642) Revert "[Kimi K3] Fuse MLA gate projection into QKV-A GEMM"
- [#33623](https://github.com/sgl-project/sglang/pull/33623) Fuse MLA gate projection into QKV-A GEMM
- plus 31 more minor config and misc updates
</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (sglang.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 876cefbc667d3174ce4af7ead7acdf4b95f1706fb2dccf2b8fde880e0e3d2aa9 -->
