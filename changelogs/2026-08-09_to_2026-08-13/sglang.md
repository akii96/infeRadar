# sglang: PR digest (2026-08-09 to 2026-08-13)

_242 merged, 321 newly opened - source sgl-project/sglang, generated 2026-08-13T10:36:52Z_

## TL;DR
- **Models**: DeepSeek (V4) and MiniMax (M3/H3) saw the most model-specific tuning, alongside massive in-flight support for Qwen 3.8 and Kimi-K3. Diffusion models (Cosmos3, LTX-2.5, Muse Glimmer, Wan2.2) received heavy optimization.
- **Performance & Kernels**: Major attention upgrades landed, including SM12x FA4 kernels, FlashInfer 0.6.17 integration, and a shift toward JIT-compiled per-token FP8 quantization.
- **Architecture**: Significant structural shifts toward unified memory pools (enabling DSPARK speculative decoding and dense KV views) and PD (Prefill/Decode) disaggregation improvements.
- **Hardware**: Broad hardware enablement expanded, notably AMD ROCm 7.2 adoption, NPU adaptations for MiniMax M3 and Kimi-K3, and MLX window-bounded SWA KV storage.

## Most important PRs
- **[#32991](https://github.com/sgl-project/sglang/pull/32991)** Adds architecture-owned SM12x FA4 kernels, introducing native FlashAttention-4 support for next-gen architectures to significantly boost attention throughput.
- **[#34613](https://github.com/sgl-project/sglang/pull/34613)** Unifies the memory read-path for attention backends (newly opened), creating a single ID-space choke point to enable seamless integration across FA3, FlashInfer, TRT-LLM, and FlashMLA.
- **[#34171](https://github.com/sgl-project/sglang/pull/34171)** Adds AdaFlash adaptive verification for DFlash speculative decoding (newly opened), optimizing acceptance rates and latency dynamically.
- **[#33997](https://github.com/sgl-project/sglang/pull/33997)** Bumps FlashInfer to 0.6.17 and removes Kimi K3 workarounds, unlocking native RMSNorm + quant fusion for SM90-SM120 and cleaning up technical debt.
- **[#34585](https://github.com/sgl-project/sglang/pull/34585)** Adds comprehensive support for Qwen 3.8 (newly opened), a massive in-flight PR enabling the model family across Triton and FlashInfer backends with speculative decoding and MoE support.

## More changes by area

<details>
<summary>Performance (11)</summary>

- [#34256](https://github.com/sgl-project/sglang/pull/34256) graph Pi0.5 prefix encoding
- [#32755](https://github.com/sgl-project/sglang/pull/32755) Occupancy tuning for DSA indexer fp8-quant Q kernel
- [#34614](https://github.com/sgl-project/sglang/pull/34614) Fuse the a2a pack/unpack copies in the MLA LSE reduce
- [#33484](https://github.com/sgl-project/sglang/pull/33484) fuse the DSv4 value and scale swap-in copy on ROCm
- [#33085](https://github.com/sgl-project/sglang/pull/33085) 128-bit non-temporal swap-in copy on ROCm
- [#34338](https://github.com/sgl-project/sglang/pull/34338) Collapse the DP attention scheduler sync to a single D2H copy
- [#34421](https://github.com/sgl-project/sglang/pull/34421) Fuse GatedDeltaNet QKVZBA split/reshape/cat into a single Triton kernel for Qwen3.5 MoE on HIP
- [#34454](https://github.com/sgl-project/sglang/pull/34454) Accelerate ROCm top-p selection and tree verification
- [#34198](https://github.com/sgl-project/sglang/pull/34198) fuse ROCm KDA decode boundary for kimi-k3
- [#34574](https://github.com/sgl-project/sglang/pull/34574) Enable symmetric-memory one-shot all-reduce on XPU
- [#34528](https://github.com/sgl-project/sglang/pull/34528) Add optional FlashInfer PCIe-IPC all-reduce for switch-free hosts on SM120

</details>

<details>
<summary>Kernels & attention (47)</summary>

- [#34148](https://github.com/sgl-project/sglang/pull/34148) SubBlock: training-free block-sparse attention for the DiT (MiniMax-H3)
- [#34329](https://github.com/sgl-project/sglang/pull/34329) HiSparse: shared-index (IndexShare) plan-then-IO swap-in prefetch
- [#34180](https://github.com/sgl-project/sglang/pull/34180) Clean up shared bitexact gates, helpers, and stale naming for diffusion
- [#34125](https://github.com/sgl-project/sglang/pull/34125) Bit-exact data-movement elimination for the Wan causal VAE decoder
- [#34275](https://github.com/sgl-project/sglang/pull/34275) Fuse Cosmos3 QK norm, RoPE, and KV packing
- [#33630](https://github.com/sgl-project/sglang/pull/33630) Add kda replayssm tests
- [#34257](https://github.com/sgl-project/sglang/pull/34257) Migrate per-token FP8 quantization from AOT to JIT
- [#34306](https://github.com/sgl-project/sglang/pull/34306) ERNIE-Image: fuse rotate-half RoPE + GELU-mul and hoist rope cos/sin
- [#34584](https://github.com/sgl-project/sglang/pull/34584) Wan2.2-TI2V: fuse per-token adaLN table add into contiguous slices + hoist rope cache
- [#34314](https://github.com/sgl-project/sglang/pull/34314) Ideogram-4: fuse Qwen3-style RoPE and SwiGLU silu-mul
- [#34172](https://github.com/sgl-project/sglang/pull/34172) LTX-2 quality=high fused RMSNorm+modulate + FFN GELU epilogue
- [#34126](https://github.com/sgl-project/sglang/pull/34126) FLUX.1: route the adaLN LN+modulate sites through the bit-exact fused LayerNorm+modulate kernel
- [#34412](https://github.com/sgl-project/sglang/pull/34412) Improve bit-exact fusion fallback diagnostics
- [#34158](https://github.com/sgl-project/sglang/pull/34158) clean up logits processor helpers
- [#33661](https://github.com/sgl-project/sglang/pull/33661) MLA Fully Support
- [#34240](https://github.com/sgl-project/sglang/pull/34240) Drop two per-layer launches from the MLA target-verify path
- [#34124](https://github.com/sgl-project/sglang/pull/34124) SYNC_STAGE_PROFILING must drain the GPU queue for stage records too
- [#34508](https://github.com/sgl-project/sglang/pull/34508) Allocate AdaLN outputs from one contiguous slab for LTX-2
- [#34431](https://github.com/sgl-project/sglang/pull/34431) Fix CUDA 13.0 VMM handle type compatibility
- [#34503](https://github.com/sgl-project/sglang/pull/34503) Tune QK head LayerNorm for SM103
- [#32954](https://github.com/sgl-project/sglang/pull/32954) cutedsl_bf16_gemm: trailing cluster barrier for 2-CTA TGV kernel exit
- [#34349](https://github.com/sgl-project/sglang/pull/34349) Tune QK head LayerNorm for SM120
- [#34372](https://github.com/sgl-project/sglang/pull/34372) Bump CuTeDSL to 4.6.2
- [#34602](https://github.com/sgl-project/sglang/pull/34602) dense KV views for uniform-row MHA/SWA models
- [#34727](https://github.com/sgl-project/sglang/pull/34727) One rmsnorm kernel for every hidden size, tuned from Python
- [#34693](https://github.com/sgl-project/sglang/pull/34693) Replace dsv3_router_gemm with the unified tiny GEMM
- [#34317](https://github.com/sgl-project/sglang/pull/34317) use tuned MXFP4 kernels for MLA absorbed BMM on GLM5
- [#34580](https://github.com/sgl-project/sglang/pull/34580) Optimize KIMI-K3 with Triton MLA decode kernel by tuning the stage-1 geometry for gfx950
- [#34429](https://github.com/sgl-project/sglang/pull/34429) Add SM120 per-tensor FP8 GEMM for small-M
- [#34617](https://github.com/sgl-project/sglang/pull/34617) Fuse eager QKV packing and high-quality QKNorm for HunyuanVideo
- [#34616](https://github.com/sgl-project/sglang/pull/34616) Fuse eager AdaLN and packed SwiGLU for FLUX.2
- [#34525](https://github.com/sgl-project/sglang/pull/34525) Gather-transpose batch KV pages for MSA sparse prefill (MiniMax-M3)
- [#34318](https://github.com/sgl-project/sglang/pull/34318) Route large SM90 row/column-scaled FP8 GEMMs to Torch
- [#34371](https://github.com/sgl-project/sglang/pull/34371) DSv4 Q norm-rope (fp8): block-per-token freq share + vectorized dequant for prefill throughput
- [#34468](https://github.com/sgl-project/sglang/pull/34468) Bound the sliding-window prefix loop and the unified-kernel KV loop on ROCm
- [#34547](https://github.com/sgl-project/sglang/pull/34547) Add one-page sparse attention paths for MiniMax-M3
- [#34387](https://github.com/sgl-project/sglang/pull/34387) Split mixed chunked-prefill FIA into prefill/decode calls on Ascend 950
- [#34646](https://github.com/sgl-project/sglang/pull/34646) Add initial Attention on Heads (AoH) runtime adapter
- [#34651](https://github.com/sgl-project/sglang/pull/34651) Share one pack kernel between both a2a backends, hoist fi_a2a send buffers
- [#34164](https://github.com/sgl-project/sglang/pull/34164) Write CuTeDSL output directly into FlashInfer A2A workspace
- [#34165](https://github.com/sgl-project/sglang/pull/34165) Fuse pending AttnRes add into direct all-gather for Kimi-K3
- [#34624](https://github.com/sgl-project/sglang/pull/34624) DSv4: fuse compress+norm+rope, emit bpreshuffle scale natively, keep kv_score in bf16 on AMD
- [#34583](https://github.com/sgl-project/sglang/pull/34583) Add MiniMax-M3 decode IndexCache on AMD
- [#34680](https://github.com/sgl-project/sglang/pull/34680) support subblock sparse attention on SM90 for Minimax H3
- [#34162](https://github.com/sgl-project/sglang/pull/34162) Add SageAttention3 packed varlen path for MiniMax-H3
- [#34385](https://github.com/sgl-project/sglang/pull/34385) selectable sequence-parallel strategies for LingBot causal attention
- [#34292](https://github.com/sgl-project/sglang/pull/34292) Fold the MXFP4 block scale in 2 instructions instead of 4 on CPU

</details>

<details>
<summary>MoE & quantization (20)</summary>

- [#33559](https://github.com/sgl-project/sglang/pull/33559) add triton moe TMA up support
- [#33669](https://github.com/sgl-project/sglang/pull/33669) Correct W4AFP8 DeepEP scaling and mode-specific dtypes
- [#34042](https://github.com/sgl-project/sglang/pull/34042) add flashinfer cute-dsl backend for mxfp8 gemm
- [#33905](https://github.com/sgl-project/sglang/pull/33905) Pad MoE expert weight row stride to avoid L3 aliasing on XPU
- [#34222](https://github.com/sgl-project/sglang/pull/34222) Support NVFP4 token embedding in ModelOpt mixed-precision checkpoints
- [#34305](https://github.com/sgl-project/sglang/pull/34305) weight-only FP8: dequantize linear weights once at first use
- [#34447](https://github.com/sgl-project/sglang/pull/34447) fused shared-expert detection PP-safe protection for Qwen
- [#34252](https://github.com/sgl-project/sglang/pull/34252) don't directly set quant class in plugins
- [#34682](https://github.com/sgl-project/sglang/pull/34682) Add CUTLASS MXFP4A8 (W4A8) grouped-GEMM MoE backend for SM90
- [#34509](https://github.com/sgl-project/sglang/pull/34509) Migrate moe_topk_softmax from AOT to JIT
- [#34698](https://github.com/sgl-project/sglang/pull/34698) implement sglang.auto_tune CLI for MoE kernel tuning
- [#34694](https://github.com/sgl-project/sglang/pull/34694) Use static FP8 communication for W4AFP8 normal dispatch in DeepEP
- [#34490](https://github.com/sgl-project/sglang/pull/34490) Add Radix-4 MoE top-k router kernel for Kimi-K3 routing on AMD
- [#34331](https://github.com/sgl-project/sglang/pull/34331) Add tuned Triton tile configs for channelwise FP8 GEMM
- [#34302](https://github.com/sgl-project/sglang/pull/34302) Support online NVFP4 for dense linear layers
- [#34277](https://github.com/sgl-project/sglang/pull/34277) Emit TMA-aligned UE8M0 scales for FP8 einsum in DSV4
- [#34540](https://github.com/sgl-project/sglang/pull/34540) Fix Quark W4A4 MXFP4 MoE clamped-SwiGLU on the AITER path
- [#34672](https://github.com/sgl-project/sglang/pull/34672) Support MegaMoE FuseEP mode for Kimi-K3 on NPU
- [#34460](https://github.com/sgl-project/sglang/pull/34460) Add gfx950 (MI350X) Triton MoE config for Kimi-K2.5 W4A16
- [#34502](https://github.com/sgl-project/sglang/pull/34502) Fuse per-token fp8 activation quant into RMSNorm for per-channel on ROCm

</details>

<details>
<summary>Model support (37)</summary>

- [#34262](https://github.com/sgl-project/sglang/pull/34262) Add Muse Glimmer model support
- [#32921](https://github.com/sgl-project/sglang/pull/32921) Add native SANA-Video T2V support
- [#31590](https://github.com/sgl-project/sglang/pull/31590) Add Cosmos3 Edge and Distilled checkpoints support
- [#34398](https://github.com/sgl-project/sglang/pull/34398) Add content-addressed preprocessing cache infrastructure for VLM
- [#34391](https://github.com/sgl-project/sglang/pull/34391) Support dynamic CPU offload components for Diffusion
- [#34243](https://github.com/sgl-project/sglang/pull/34243) Serve Cosmos3 policies through the Action API
- [#33921](https://github.com/sgl-project/sglang/pull/33921) Preprocess CPU-transport images on the vision owner for Kimi K3
- [#34563](https://github.com/sgl-project/sglang/pull/34563) Optimize bit-exact H3 reference video ingress
- [#34249](https://github.com/sgl-project/sglang/pull/34249) move DiT execution capabilities to runtime models
- [#34564](https://github.com/sgl-project/sglang/pull/34564) Stream and parallelize bit-exact video output saves
- [#34175](https://github.com/sgl-project/sglang/pull/34175) Replace deprecated image processor use_fast
- [#34359](https://github.com/sgl-project/sglang/pull/34359) Support native and PEFT MiniMax H3 LoRAs
- [#34064](https://github.com/sgl-project/sglang/pull/34064) Optimize ordinary model weight loading for Diffusion
- [#34136](https://github.com/sgl-project/sglang/pull/34136) Add online FP8 support for Krea-2
- [#34143](https://github.com/sgl-project/sglang/pull/34143) refresh skills for latest runtime for diffusion
- [#34248](https://github.com/sgl-project/sglang/pull/34248) expose architecture config at the DiT runtime boundary
- [#34294](https://github.com/sgl-project/sglang/pull/34294) Fix H3 rank-local FSDP QKV loading
- [#34141](https://github.com/sgl-project/sglang/pull/34141) Reserve multimodal runtime allocations and keep padded inputs aligned
- [#34512](https://github.com/sgl-project/sglang/pull/34512) suppress noisy worker startup warnings for diffusion
- [#34411](https://github.com/sgl-project/sglang/pull/34411) Reuse cached Kimi-K3 embeddings before preprocessing
- [#34471](https://github.com/sgl-project/sglang/pull/34471) Support LTX-2.5
- [#34404](https://github.com/sgl-project/sglang/pull/34404) Cache Kimi-K3 per-image processor artifacts
- [#34188](https://github.com/sgl-project/sglang/pull/34188) Rust Kimi-K3 image preprocessing in sglang-mm (library mode)
- [#34599](https://github.com/sgl-project/sglang/pull/34599) Optimize Pi0.5 inference and bounded graph serving
- [#34588](https://github.com/sgl-project/sglang/pull/34588) Bound Pi0.5 CUDA graphs with prompt buckets
- [#34650](https://github.com/sgl-project/sglang/pull/34650) rebuild MiniMax-H3 AdaLN outputs on demand
- [#34534](https://github.com/sgl-project/sglang/pull/34534) Add --dit-layerwise-residency-policy for strided DiT residency
- [#34416](https://github.com/sgl-project/sglang/pull/34416) Preserve per-sample rollout trajectories across multi-output merge
- [#34494](https://github.com/sgl-project/sglang/pull/34494) Forward multimodal token type IDs in image encoding
- [#34615](https://github.com/sgl-project/sglang/pull/34615) Make auto residency decisions component-scoped
- [#34154](https://github.com/sgl-project/sglang/pull/34154) Give multimodal draft-extend one mRoPE position per extended token
- [#34170](https://github.com/sgl-project/sglang/pull/34170) Add FastSafetensors sharded-state loader
- [#34418](https://github.com/sgl-project/sglang/pull/34418) Apply latent-ids and packing to caller-provided initial latents
- [#34581](https://github.com/sgl-project/sglang/pull/34581) Optimizing MiniMax-H3 for consumer-level GPUs: INT8 Linear + pluggable DiT attention backends
- [#34365](https://github.com/sgl-project/sglang/pull/34365) support MiniMax H3 RL
- [#34197](https://github.com/sgl-project/sglang/pull/34197) RL rollout support for the Cosmos3 pipeline
- [#34713](https://github.com/sgl-project/sglang/pull/34713) Allow encoder DP under DiT tensor parallelism

</details>

<details>
<summary>Parallelism & scheduling (40)</summary>

- [#34166](https://github.com/sgl-project/sglang/pull/34166) Window-bounded SWA KV storage and in-graph sampling for MLX
- [#33362](https://github.com/sgl-project/sglang/pull/33362) Support --enable-unified-memory with PD disaggregation
- [#30827](https://github.com/sgl-project/sglang/pull/30827) add cache salt support to KV cache events
- [#34206](https://github.com/sgl-project/sglang/pull/34206) Pipeline owner-only multimodal preprocessing
- [#30023](https://github.com/sgl-project/sglang/pull/30023) sglang tracing v2: support exporting tracing data asynchronously
- [#33974](https://github.com/sgl-project/sglang/pull/33974) Support DSPARK speculative decoding + fix two NaN root causes
- [#33807](https://github.com/sgl-project/sglang/pull/33807) Support pipeline-parallel prefill with Mooncake staging buffer
- [#34234](https://github.com/sgl-project/sglang/pull/34234) Budget the DFLASH draft KV pool from its own attention geometry
- [#33477](https://github.com/sgl-project/sglang/pull/33477) Reuse batched Mamba boundary mask
- [#33910](https://github.com/sgl-project/sglang/pull/33910) Refactor staging registration metadata fields
- [#33639](https://github.com/sgl-project/sglang/pull/33639) Support Mamba branching in Unified Radix Cache with HiCache
- [#34080](https://github.com/sgl-project/sglang/pull/34080) retire the hidden global fallbacks and the mamba-extra-buffer instance reads
- [#34133](https://github.com/sgl-project/sglang/pull/34133) derive the runner's DCP topology from its ParallelState
- [#34407](https://github.com/sgl-project/sglang/pull/34407) Worker Snapshot Support for Recoverable KV Placement State in sgl-router
- [#34299](https://github.com/sgl-project/sglang/pull/34299) Close Phase A CAKE engagement and zero-copy admission
- [#34623](https://github.com/sgl-project/sglang/pull/34623) Concurrent chunked prefill via --long-prefill-token-threshold
- [#34337](https://github.com/sgl-project/sglang/pull/34337) Support multi-adapter LoRA with EAGLE/NEXTN/DFLASH/DSPARK speculative decoding
- [#34569](https://github.com/sgl-project/sglang/pull/34569) PP prefill: ordered immutable bootstrap decisions with exactly-once apply
- [#34201](https://github.com/sgl-project/sglang/pull/34201) DFlash: top-p mask capture
- [#34402](https://github.com/sgl-project/sglang/pull/34402) Add distributed exact input logprobs
- [#34704](https://github.com/sgl-project/sglang/pull/34704) Add distributed exact prompt Top-N logprobs
- [#34311](https://github.com/sgl-project/sglang/pull/34311) Read the draft checkpoint config with the target's resolution inputs
- [#34355](https://github.com/sgl-project/sglang/pull/34355) Support decode context parallelism (DCP) on Intel XPU
- [#34369](https://github.com/sgl-project/sglang/pull/34369) Stream weights over HTTP Range with one NIC per TP rank
- [#34406](https://github.com/sgl-project/sglang/pull/34406) TP/PP Consensus checker
- [#34608](https://github.com/sgl-project/sglang/pull/34608) Publish per-scheduler load on a dedicated socket for load-aware routers
- [#34343](https://github.com/sgl-project/sglang/pull/34343) Support PD disaggregation with DCP + DSPARK
- [#34290](https://github.com/sgl-project/sglang/pull/34290) Derive the speculative max_running_requests default from the decode CUDA-graph ladder
- [#34625](https://github.com/sgl-project/sglang/pull/34625) Remove GPU rendezvous from symmetric DP metadata sync
- [#34373](https://github.com/sgl-project/sglang/pull/34373) Add a one-sided symmetric-memory path for the DP metadata gather
- [#34565](https://github.com/sgl-project/sglang/pull/34565) Support swa branching-point caching in Unified Radix Cache
- [#34568](https://github.com/sgl-project/sglang/pull/34568) PP prefill: fold HiCache prefetch readiness into the bootstrap consensus
- [#34320](https://github.com/sgl-project/sglang/pull/34320) count waiting-queue request rejections
- [#34414](https://github.com/sgl-project/sglang/pull/34414) Unify the request length validation logic
- [#34185](https://github.com/sgl-project/sglang/pull/34185) Drop requests that are already too stale during a weight-update pause
- [#34570](https://github.com/sgl-project/sglang/pull/34570) PD: never auto-replay a request that may already be dispatched
- [#34216](https://github.com/sgl-project/sglang/pull/34216) Handle terminal decode streams in P/D model gateway
- [#34724](https://github.com/sgl-project/sglang/pull/34724) Batch final DSV4 draft SWA transfer
- [#34285](https://github.com/sgl-project/sglang/pull/34285) Support DFlash speculative decoding under PD disaggregation
- [#34665](https://github.com/sgl-project/sglang/pull/34665) Expose DP-attention MLP sync transport

</details>

<details>
<summary>Hardware & arch (23)</summary>

- [#32941](https://github.com/sgl-project/sglang/pull/32941) Adaptation of Minimax M3(w8a8) for NPU platforms
- [#34379](https://github.com/sgl-project/sglang/pull/34379) GLM 5.2 MXFP4 SGLANG COOKBOOK for AMD
- [#33465](https://github.com/sgl-project/sglang/pull/33465) Support Kimi-K3 on NPU
- [#30050](https://github.com/sgl-project/sglang/pull/30050) Support gpt-oss: sliding-window attention, attention sinks, sm_scale on MLX
- [#34204](https://github.com/sgl-project/sglang/pull/34204) Swap the AMD PR gate to ROCm 7.2 and demote ROCm 7.0 to a daily shadow
- [#30700](https://github.com/sgl-project/sglang/pull/30700) Add flashinfer MNNVL backend for allreduce only on NVIDIA
- [#31105](https://github.com/sgl-project/sglang/pull/31105) Fix fp8 per-channel attention for Kimi-K2.7-code-mxfp4 on ROCm/gfx95
- [#34328](https://github.com/sgl-project/sglang/pull/34328) CI: fix AMD 2-GPU multimodal-gen partition-count abort
- [#33484](https://github.com/sgl-project/sglang/pull/33484) fuse the DSv4 value and scale swap-in copy on ROCm
- [#34476](https://github.com/sgl-project/sglang/pull/34476) Add GLM-5.2 MXFP4 wide-EP16 2P1D nightly recipes for AMD
- [#34261](https://github.com/sgl-project/sglang/pull/34261) Restore K3 MLA verify kernel path blocked by can_handle() guard on AMD
- [#34597](https://github.com/sgl-project/sglang/pull/34597) Run V4 MTP target-verify through the decode kernel on AMD
- [#34673](https://github.com/sgl-project/sglang/pull/34673) Restore KTransformers CPU-expert offload for DeepSeek-V4 on Ascend NPU
- [#34537](https://github.com/sgl-project/sglang/pull/34537) Add gluon path for aiter backend on AMD
- [#34454](https://github.com/sgl-project/sglang/pull/34454) Accelerate ROCm top-p selection and tree verification
- [#34140](https://github.com/sgl-project/sglang/pull/34140) Enable stochastic tree verification on ROCm
- [#34432](https://github.com/sgl-project/sglang/pull/34432) add dcp support for aiter backend on AMD
- [#34647](https://github.com/sgl-project/sglang/pull/34647) Enable 12-head MLA aiter fp8 Gluon decode on AMD
- [#34200](https://github.com/sgl-project/sglang/pull/34200) Port CP V2 to the DeepSeek-V4 HIP backend
- [#34394](https://github.com/sgl-project/sglang/pull/34394) Fuse the ROCm DSA indexer q/k prep into aiter's single kernel
- [#34517](https://github.com/sgl-project/sglang/pull/34517) Accelerate Qwen3.5 verification with grouped-head shared KV on AMD
- [#34393](https://github.com/sgl-project/sglang/pull/34393) Enable IBM Power (ppc64le) support
- [#34425](https://github.com/sgl-project/sglang/pull/34425) Accept XPU in the shared test CLI --device choices
- [#34293](https://github.com/sgl-project/sglang/pull/34293) Add NpuSRTPlatform so current_platform resolves on Ascend

</details>

<details>
<summary>API & serving (16)</summary>

- [#34246](https://github.com/sgl-project/sglang/pull/34246) S3 token dataset export for offline cache-hit analysis
- [#34228](https://github.com/sgl-project/sglang/pull/34228) support --served-model-name in sglang serve
- [#30392](https://github.com/sgl-project/sglang/pull/30392) Decouple multimodal global cache from Mooncake
- [#34326](https://github.com/sgl-project/sglang/pull/34326) Add MegaMoE runner compatibility alias
- [#34652](https://github.com/sgl-project/sglang/pull/34652) publish an index of nightly comparison runs for diffusion
- [#34655](https://github.com/sgl-project/sglang/pull/34655) track MiniMax-H3 in the nightly diffusion benchmark
- [#34687](https://github.com/sgl-project/sglang/pull/34687) Main transport
- [#34533](https://github.com/sgl-project/sglang/pull/34533) Add --tokenizer-backend=gigatoken: ~50x faster prompt encode, byte-identical
- [#34707](https://github.com/sgl-project/sglang/pull/34707) Main transport1
- [#34488](https://github.com/sgl-project/sglang/pull/34488) Add response-level input/output token ids to chat completions via SglExt
- [#34224](https://github.com/sgl-project/sglang/pull/34224) support preferred sampling params in rust-server
- [#34553](https://github.com/sgl-project/sglang/pull/34553) add --enable-sort-tool-schema-keys to share prefix cache across tool key orders
- [#34699](https://github.com/sgl-project/sglang/pull/34699) separate input_ids from control plane message in rust-server
- [#34721](https://github.com/sgl-project/sglang/pull/34721) Unify MM feature transport on POSIX shm (drop inline mode)
- [#34430](https://github.com/sgl-project/sglang/pull/34430) Use node-local HTTP ports for DP attention in rust-server
- [#34531](https://github.com/sgl-project/sglang/pull/34531) support `save_remote_model` and `save_sharded_model` in rust-server

</details>

<details>
<summary>Tests, CI & build (39)</summary>

- [#34520](https://github.com/sgl-project/sglang/pull/34520) Remove 22 unmaintained benchmarks
- [#34186](https://github.com/sgl-project/sglang/pull/34186) Key scheduled CUDA suites by runner_config instead of hand-written jobs
- [#34464](https://github.com/sgl-project/sglang/pull/34464) Refocus LoRA tests on regression coverage
- [#34477](https://github.com/sgl-project/sglang/pull/34477) Route mmlu and GB300 MMMU-Pro evals through sgl-eval
- [#34380](https://github.com/sgl-project/sglang/pull/34380) Add a scheduled workflow to close stale PRs
- [#34276](https://github.com/sgl-project/sglang/pull/34276) Build patched Docker images for both amd64 and arm64
- [#34253](https://github.com/sgl-project/sglang/pull/34253) Add output_tag input to the Patch Docker Image workflow
- [#34635](https://github.com/sgl-project/sglang/pull/34635) Use default installer for B300 tests
- [#34669](https://github.com/sgl-project/sglang/pull/34669) Split Kimi K2.5 performance batches by config
- [#34671](https://github.com/sgl-project/sglang/pull/34671) Add New Intel members into CI permission list
- [#34147](https://github.com/sgl-project/sglang/pull/34147) Register the DeepSeek-V4-Pro-DSpark MI35x nightly job so its suite actually runs
- [#34364](https://github.com/sgl-project/sglang/pull/34364) Install AITER's pinned Triton wheel in the ROCm 7.2 image
- [#34191](https://github.com/sgl-project/sglang/pull/34191) Skip speculative verify scratch on prefill servers
- [#34231](https://github.com/sgl-project/sglang/pull/34231) Keep the torch compilation cache instead of wiping it on install
- [#34195](https://github.com/sgl-project/sglang/pull/34195) Align rerun-test environment with the test stages
- [#34247](https://github.com/sgl-project/sglang/pull/34247) Standardize diffusion cookbook model pages
- [#34270](https://github.com/sgl-project/sglang/pull/34270) config: the runner-side instance reads finish converging (not for merge)
- [#34274](https://github.com/sgl-project/sglang/pull/34274) Content-addressed JIT build cache, generated from our own ninja
- [#34544](https://github.com/sgl-project/sglang/pull/34544) Route test empty_cache and synchronize in device-agnostic tests
- [#34556](https://github.com/sgl-project/sglang/pull/34556) Model serve pr/mamba 2 and 1
- [#34196](https://github.com/sgl-project/sglang/pull/34196) update CI test est_time values
- [#34309](https://github.com/sgl-project/sglang/pull/34309) Prune redundant CPU test overhead
- [#34501](https://github.com/sgl-project/sglang/pull/34501) Support sglang-kernel on Windows ARM64
- [#34708](https://github.com/sgl-project/sglang/pull/34708) Add perf and acc test for CPU models for nightly
- [#34516](https://github.com/sgl-project/sglang/pull/34516) Disable most NPU nightly tests, keep only minimax and qwen3_235b cases
- [#34493](https://github.com/sgl-project/sglang/pull/34493) Add unit tests for reasoning_parser
- [#34229](https://github.com/sgl-project/sglang/pull/34229) Add minimal PR smoke test framework
- [#34487](https://github.com/sgl-project/sglang/pull/34487) cache the CI image instead of re-pulling it in every job on AMD
- [#34288](https://github.com/sgl-project/sglang/pull/34288) Add CPU unit tests for serving_rerank
- [#34439](https://github.com/sgl-project/sglang/pull/34439) Add focused CPU-only unit tests for InklingDetector
- [#34706](https://github.com/sgl-project/sglang/pull/34706) Add unit tests for utils/field_validators
- [#34332](https://github.com/sgl-project/sglang/pull/34332) Add unit tests for srt/managers/scheduler_components/idle_sleeper.py
- [#34483](https://github.com/sgl-project/sglang/pull/34483) cut two setup cycles from the AMD multimodal-gen lanes
- [#34504](https://github.com/sgl-project/sglang/pull/34504) Support SGLang on Windows ARM64
- [#34342](https://github.com/sgl-project/sglang/pull/34342) extract proto generation
- [#34645](https://github.com/sgl-project/sglang/pull/34645) Add GPT-OSS and Kimi-K3 ROCm 7.2 perf benchmarks
- [#34643](https://github.com/sgl-project/sglang/pull/34643) Stop scheduling Grok-1 and Grok-2 on MI30x
- [#34586](https://github.com/sgl-project/sglang/pull/34586) Pre-build AITER JIT kernels after a forced AITER rebuild
- plus 1 more minor CI update

</details>

<details>
<summary>Docs (19)</summary>

- [#34587](https://github.com/sgl-project/sglang/pull/34587) Add Qwen3.8 cookbook
- [#34271](https://github.com/sgl-project/sglang/pull/34271) Muse Glimmer Cookbook
- [#33820](https://github.com/sgl-project/sglang/pull/33820) Add Intern-S2-Mobius cookbook
- [#33481](https://github.com/sgl-project/sglang/pull/33481) Add NVIDIA Nemotron 3.5 Lightning cookbook
- [#30223](https://github.com/sgl-project/sglang/pull/30223) Add Hunyuan3 On Ascend Doc
- [#34283](https://github.com/sgl-project/sglang/pull/34283) Cookbook: add Ling-3.0-tiny
- [#34175](https://github.com/sgl-project/sglang/pull/34175) Replace deprecated image processor use_fast
- [#34573](https://github.com/sgl-project/sglang/pull/34573) add BF16 recipes to Nemotron 3.5 Lightning
- [#34097](https://github.com/sgl-project/sglang/pull/34097) record where config is read now that the seed is off limits
- [#34363](https://github.com/sgl-project/sglang/pull/34363) Add Ling-3.0-flash INT4 and MXFP4 recipes
- [#34395](https://github.com/sgl-project/sglang/pull/34395) Add Ling-3.0-tiny INT4 recipes
- [#34497](https://github.com/sgl-project/sglang/pull/34497) Update Cosmos3 Edge and distilled cookbook
- [#34601](https://github.com/sgl-project/sglang/pull/34601) update Qwen3.8 disaggregated serving configs
- [#34590](https://github.com/sgl-project/sglang/pull/34590) Rename Qwen3.8-Max-DSpark to Qwen3.8-2.4T-A95B-DSpark
- [#34323](https://github.com/sgl-project/sglang/pull/34323) Muse Glimmer cookbook: drop --speculative-dflash-block-size 5
- [#34176](https://github.com/sgl-project/sglang/pull/34176) document the request-level quality parameter for diffusion
- [#34654](https://github.com/sgl-project/sglang/pull/34654) Add decode context parallelism to advanced features
- [#34658](https://github.com/sgl-project/sglang/pull/34658) add new cookbooks
- [#34269](https://github.com/sgl-project/sglang/pull/34269) state the bag contract as what resolution produced, and the skill rule that goes with it

</details>

<details>
<summary>Bugfixes (40)</summary>

- [#33949](https://github.com/sgl-project/sglang/pull/33949) stream-order CUDA IPC feature pool lifecycle and streamline multimodal transport module
- [#30762](https://github.com/sgl-project/sglang/pull/30762) support DeepSeek-V4 hybrid HostPoolGroup
- [#34458](https://github.com/sgl-project/sglang/pull/34458) Make DeepSeek-V4 reasoning and tool-call streaming parsing chunk-invariant
- [#34523](https://github.com/sgl-project/sglang/pull/34523) Fix nightly test failures
- [#34189](https://github.com/sgl-project/sglang/pull/34189) Fix silent KV corruption when speculative draft tokens > 4
- [#34219](https://github.com/sgl-project/sglang/pull/34219) Revert "feat(cache-sim-tee): concurrent ingest sender"
- [#33436](https://github.com/sgl-project/sglang/pull/33436) support FA4 backend for GLM4.7-flash
- [#34163](https://github.com/sgl-project/sglang/pull/34163) preserve Kimi-K3 GPU JPEG accuracy
- [#28753](https://github.com/sgl-project/sglang/pull/28753) Fix/hisparse host backed max request length
- [#34167](https://github.com/sgl-project/sglang/pull/34167) Fix top-k v2 dropping non-primary ranks' output on CUDA 13.1+
- [#34401](https://github.com/sgl-project/sglang/pull/34401) Fix model-driven DiT layerwise offload auto policy
- [#34294](https://github.com/sgl-project/sglang/pull/34294) Fix H3 rank-local FSDP QKV loading
- [#33517](https://github.com/sgl-project/sglang/pull/33517) Fix NaN logits from deterministic Triton extend on the unified memory pool
- [#33312](https://github.com/sgl-project/sglang/pull/33312) Fix DSV4 DSpark shared expert loading
- [#34662](https://github.com/sgl-project/sglang/pull/34662) restore VLM nightly regression coverage
- [#29792](https://github.com/sgl-project/sglang/pull/29792) Fix Mamba track-boundary bookkeeping under overlap scheduling
- [#33865](https://github.com/sgl-project/sglang/pull/33865) Fix DSpark + DeepSeek V4 prefill CP compatibility
- [#34347](https://github.com/sgl-project/sglang/pull/34347) Fix SM120 QKNorm+RoPE rounding for MiniMax H3
- [#34210](https://github.com/sgl-project/sglang/pull/34210) Z-Image single-GPU BCG: fix the replay crash and make output bit-exact vs eager
- [#34161](https://github.com/sgl-project/sglang/pull/34161) preserve GQA head mapping in Triton DCP prefill
- [#33940](https://github.com/sgl-project/sglang/pull/33940) route scheduler aborts to multi-tokenizer workers
- [#32685](https://github.com/sgl-project/sglang/pull/32685) update weight from tensor detects device by uuid
- [#34301](https://github.com/sgl-project/sglang/pull/34301) Fix CI server warmup progress logging
- [#30394](https://github.com/sgl-project/sglang/pull/30394) make automatic NUMA binding configurable
- [#33075](https://github.com/sgl-project/sglang/pull/33075) Allow flashinfer_sparse_mla DSA backend for HiSparse on SM120 FP8 KV
- [#34423](https://github.com/sgl-project/sglang/pull/34423) nightly diffusion benchmark passes the retired --warmup flag
- [#32227](https://github.com/sgl-project/sglang/pull/32227) Fix NemotronH (hybrid mamba2) launch on --device xpu
- [#34341](https://github.com/sgl-project/sglang/pull/34341) Fix HiCache MHA backup for NPU
- [#34524](https://github.com/sgl-project/sglang/pull/34524) Fix DFlash sliding attention causality defaults
- [#34405](https://github.com/sgl-project/sglang/pull/34405) Fix flaky decode cache-hit check in Inkling test
- [#31700](https://github.com/sgl-project/sglang/pull/31700) Fix DeepSeek-V4/DeepSeek-V4-Pro DP-attention gather semantics
- [#34443](https://github.com/sgl-project/sglang/pull/34443) Fix num_splits "(b+1)" crash on prefill-CP speculative decode
- [#34500](https://github.com/sgl-project/sglang/pull/34500) Fix tokenizer warning filtering for processors
- [#34159](https://github.com/sgl-project/sglang/pull/34159) Fix deterministic inference all-reduce for tp>1
- [#34637](https://github.com/sgl-project/sglang/pull/34637) Fix nightly test failures
- [#33912](https://github.com/sgl-project/sglang/pull/33912) account for DCP in draft KV pool sizing
- [#34289](https://github.com/sgl-project/sglang/pull/34289) Fix NIXL P/D serving stall after prefill replacement
- [#34237](https://github.com/sgl-project/sglang/pull/34237) lfm2 detector: recover tool calls dropped by common model-output
- [#34685](https://github.com/sgl-project/sglang/pull/34685) stream MiMo tool call arguments incrementally
- plus 33 more minor bugfixes

</details>

<details>
<summary>Refactors (15)</summary>

- [#34081](https://github.com/sgl-project/sglang/pull/34081) business code no longer reads the published ServerArgs
- [#33894](https://github.com/sgl-project/sglang/pull/33894) refactor error responses into shared utils::response helpers
- [#34160](https://github.com/sgl-project/sglang/pull/34160) Revert parallel request lifecycle tracking from #32588
- [#34472](https://github.com/sgl-project/sglang/pull/34472) Sanitize the structure of environ.py
- [#34336](https://github.com/sgl-project/sglang/pull/34336) Split the FlashInfer autotune dummy-run flag from the LM-head policy
- [#34312](https://github.com/sgl-project/sglang/pull/34312) extract request conversion for anthropic
- [#34313](https://github.com/sgl-project/sglang/pull/34313) extract response conversion for anthropic
- [#34660](https://github.com/sgl-project/sglang/pull/34660) refactor mm code for rust tokenizer manager
- [#34515](https://github.com/sgl-project/sglang/pull/34515) Avoid host synchronization in sparse prefill cleanup for DSV4
- [#34267](https://github.com/sgl-project/sglang/pull/34267) pin the supplied-instance surface that a raw record would change
- [#34264](https://github.com/sgl-project/sglang/pull/34264) decisions keyed on the attention backend read the configured pair
- [#34266](https://github.com/sgl-project/sglang/pull/34266) the alias form of the runner-side instance read
- [#34263](https://github.com/sgl-project/sglang/pull/34263) the last runner-side instance reads read the bags
- [#34265](https://github.com/sgl-project/sglang/pull/34265) a named entry point for the resolution pipeline, and the last dynamic config read
- [#34268](https://github.com/sgl-project/sglang/pull/34268) the post-publish consumers of the pinned surface read the bags

</details>

<details>
<summary>Other (22)</summary>

- [#33895](https://github.com/sgl-project/sglang/pull/33895) move the PD bootstrap registry under api_server::disaggregation
- [#26671](https://github.com/sgl-project/sglang/pull/26671) Optimize epilogue of c128 for DSv4
- [#34094](https://github.com/sgl-project/sglang/pull/34094) pin that resolution is reproducible from the raw input
- [#34096](https://github.com/sgl-project/sglang/pull/34096) the KV-cache configurator reads the bags
- [#34095](https://github.com/sgl-project/sglang/pull/34095) the runner and scheduler read resolved config from the bags
- [#34169](https://github.com/sgl-project/sglang/pull/34169) Add skill for the logprob consistency tests
- [#34607](https://github.com/sgl-project/sglang/pull/34607) Add bit-exact unified radix cache KL test for hybrid SWA + mamba
- [#34356](https://github.com/sgl-project/sglang/pull/34356) Add bit-exact hicache logprob-consistency test
- [#34168](https://github.com/sgl-project/sglang/pull/34168) Add deterministic logprob-consistency test for inkling-small nvfp4
- [#32402](https://github.com/sgl-project/sglang/pull/32402) Switch inkling per-commit test to nvfp4
- [#34656](https://github.com/sgl-project/sglang/pull/34656) Record both architectures in the bit-exact guard docstrings
- [#32208](https://github.com/sgl-project/sglang/pull/32208) O(1) slot allocation in ReqToTokenPool.alloc()
- [#34335](https://github.com/sgl-project/sglang/pull/34335) don't clock-rebase unset time sentinels in ReqTimeStats deserialization
- [#34667](https://github.com/sgl-project/sglang/pull/34667) Drop the mmlu case from the unified radix cache kit
- [#34538](https://github.com/sgl-project/sglang/pull/34538) Reenable breakable CUDA graph for NemotronH
- [#33662](https://github.com/sgl-project/sglang/pull/33662) Avoid host syncs in EAGLE prefill for DSV4
- [#34173](https://github.com/sgl-project/sglang/pull/34173) Make torch.compile opt-in for speed mode for diffusion
- [#34174](https://github.com/sgl-project/sglang/pull/34174) auto-capture the default warmup resolution instead of hard-requiring --warmup-resolutions
- [#33146](https://github.com/sgl-project/sglang/pull/33146) Support thinking budget for Inkling
- [#34225](https://github.com/sgl-project/sglang/pull/34225) Release LoRARegistry reference for aborted requests
- [#34428](https://github.com/sgl-project/sglang/pull/34428) Honor should_apply_lora when wrapping LoRA target modules
- [#34726](https://github.com/sgl-project/sglang/pull/34726) Feiyue/mori pp dcp

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (sglang.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 6f6911917fb40f8e2401032914e3ba942463c42af78329efbd989ef508652852 -->
