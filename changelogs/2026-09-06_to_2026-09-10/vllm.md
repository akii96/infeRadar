# vllm: PR digest (2026-09-06 to 2026-09-10)

_207 merged, 466 newly opened - source vllm-project/vllm, generated 2026-09-10T13:39:18Z_

## TL;DR
- **DeepSeek-V4 / V4.1-Flash dominated the window.** On the merge side: V4.1-Flash model definitions (`[#56228](https://github.com/vllm-project/vllm/pull/56228)`), a CPU backend (`[#55355](https://github.com/vllm-project/vllm/pull/55355)`), Rust/Python frontend support (`[#56208](https://github.com/vllm-project/vllm/pull/56208)`) and the "warmup" kernel-migration series (`[#50176](https://github.com/vllm-project/vllm/pull/50176)`, `[#53564](https://github.com/vllm-project/vllm/pull/53564)`, `[#53565](https://github.com/vllm-project/vllm/pull/53565)`). Newly opened: the full V4.1 integration (`[#56214](https://github.com/vllm-project/vllm/pull/56214)`), an SM80 Triton fallback (`[#56120](https://github.com/vllm-project/vllm/pull/56120)`) and DeepGEMM Mega-Gate/Mega-mHC/sparse-MQA indexer work (`[#56266](https://github.com/vllm-project/vllm/pull/56266)`, `[#56255](https://github.com/vllm-project/vllm/pull/56255)`, `[#56254](https://github.com/vllm-project/vllm/pull/56254)`).
- **Perf work centers on linear-attention and sparse-attention kernels.** Merged: FlashInfer KDA kernels (`[#55364](https://github.com/vllm-project/vllm/pull/55364)`), ROCm KDA prefill for Kimi-K3 (`[#54038](https://github.com/vllm-project/vllm/pull/54038)`), a 5.2–7.7% E2E gain from avoiding KDA mixed-batch gather/scatter (`[#56159](https://github.com/vllm-project/vllm/pull/56159)`), and AITER sparse-attention scoring for MiniMax-M3 (`[#52664](https://github.com/vllm-project/vllm/pull/52664)`). Opened: Mamba/GDN batched grouped prefill (+7.58x, `[#55876](https://github.com/vllm-project/vllm/pull/55876)`).
- **Quantization and MoE keep moving.** The merged set includes a router-GEMM accuracy fix on sm100 (`[#55899](https://github.com/vllm-project/vllm/pull/55899)`), Quark per-block FP8 MoE (`[#52263](https://github.com/vllm-project/vllm/pull/52263)`), DSv4 MXFP4+FP8 shared-expert fusion on ROCm (`[#53161](https://github.com/vllm-project/vllm/pull/53161)`) and a large GPTQ cleanup (`[#54809](https://github.com/vllm-project/vllm/pull/54809)`). Opened: shared GPU expert pool for NVFP4 Marlin offload (`[#56177](https://github.com/vllm-project/vllm/pull/56177)`) and RDNA4 FP8 block-scale FlyDSL kernels (`[#56005](https://github.com/vllm-project/vllm/pull/56005)`).
- **Direction:** more model families brought up on more hardware (CPU, ROCm/RDNA, XPU, Ampere), a Rust frontend taking over, and KV-offload/EC-connector/disaggregation robustness.

## Most important PRs
**[#56228](https://github.com/vllm-project/vllm/pull/56228) - DeepSeek-V4.1-Flash model definitions.** Merged. Adds the V4.1 model code with attention, quantization, spec-decode and multimodal hooks for NVIDIA and AMD. This is the foundation for the in-flight `[#56214](https://github.com/vllm-project/vllm/pull/56214)` integration.

**[#55355](https://github.com/vllm-project/vllm/pull/55355) - DeepSeek-V4 CPU backend.** Merged. Brings V4 to CPU with attention, MoE and quantization paths, so the model no longer needs a GPU.

**[#54038](https://github.com/vllm-project/vllm/pull/54038) - ROCm fused KDA prefill kernels for Kimi-K3.** Merged. Adds fused kernels for the KDA linear-attention prefill path on AMD; `#36036`-style follow-ups continue in open `[#56036](https://github.com/vllm-project/vllm/pull/56036)`, which uses AITER KDA prefill.

**[#54809](https://github.com/vllm-project/vllm/pull/54809) - Remove GPTQ group/dynamic activation ordering.** Merged. Drops about 3.9k lines across 99 files and all backends (CUDA, ROCm, CPU, XPU). This shrinks the kernel surface that quant work has to maintain.

**[#56159](https://github.com/vllm-project/vllm/pull/56159) - Avoid KDA mixed-batch gather/scatter in Kimi K3.** Merged. Removes the copy overhead in mixed prefill/decode batches, for a measured 5.2–7.7% end-to-end throughput gain.

## More changes by area

<details>
<summary>Performance (14)</summary>

- [#55364](https://github.com/vllm-project/vllm/pull/55364) integrate FlashInfer KDA kernels
- [#55899](https://github.com/vllm-project/vllm/pull/55899) BF16x3 router GEMM accuracy fix, default on sm100
- [#55736](https://github.com/vllm-project/vllm/pull/55736) GLM-5.3-Flash decode hot-path cleanups (strided KDA inputs, no duplicate router GEMM)
- [#55223](https://github.com/vllm-project/vllm/pull/55223) eliminate full-history reasoning scans for structured outputs
- [#54797](https://github.com/vllm-project/vllm/pull/54797) extend Qwen Triton warmup to avoid first-request latency spikes
- [#55629](https://github.com/vllm-project/vllm/pull/55629) fuse DeepEncoder relative bias in Triton attention
- [#55499](https://github.com/vllm-project/vllm/pull/55499) fix TRTLLM ragged prefill perf regression
- [#55715](https://github.com/vllm-project/vllm/pull/55715) enable FlashInfer GDN prefill kernel on SM12x
- [#55170](https://github.com/vllm-project/vllm/pull/55170) prefer W4A4 NVFP4 linear kernels on SM120/121
- [#54668](https://github.com/vllm-project/vllm/pull/54668) tune H20 block-FP8 MoE low-batch configs (+21%)
- [#55285](https://github.com/vllm-project/vllm/pull/55285) use SDPA for BLIP-2 Q-Former attention
- [#55965](https://github.com/vllm-project/vllm/pull/55965) speed up vLLM IR test group
- [#55731](https://github.com/vllm-project/vllm/pull/55731) reduce NPU CI time and add timeout
- [#45900](https://github.com/vllm-project/vllm/pull/45900) fix Qwen3 audio encoder TP when heads aren't divisible by TP size

</details>

<details>
<summary>Kernels & attention (12)</summary>

- [#50176](https://github.com/vllm-project/vllm/pull/50176) migrate common DSv4 attention kernels (warmup 4/N)
- [#53564](https://github.com/vllm-project/vllm/pull/53564) migrate DSv4 sequence and DCP kernels (warmup 2/N)
- [#53565](https://github.com/vllm-project/vllm/pull/53565) migrate FA4 MLA and shared CuTeDSL kernels (warmup 3/N)
- [#56215](https://github.com/vllm-project/vllm/pull/56215) optional Q-norm in fused DSv4 MLA epilogue; group_size=32 packed FP8 quant
- [#54855](https://github.com/vllm-project/vllm/pull/54855) route large DSv4 sparse prefill to AITER OPUS on ROCm
- [#54404](https://github.com/vllm-project/vllm/pull/54404) attention-sink support in ROCm AITER sparse MLA
- [#55808](https://github.com/vllm-project/vllm/pull/55808) remove AITER paged-MQA outputs guard for DSv4
- [#55755](https://github.com/vllm-project/vllm/pull/55755) PDL enablement for fusedQKNormRopeKernel
- [#55180](https://github.com/vllm-project/vllm/pull/55180) SM12x blockwise FP8: swizzle CTA raster when weight exceeds L2
- [#49410](https://github.com/vllm-project/vllm/pull/49410) native AMX-FP8 attention for Diamond Rapids CPU
- [#55780](https://github.com/vllm-project/vllm/pull/55780) require explicit DCP support from attention implementations
- [#55888](https://github.com/vllm-project/vllm/pull/55888) avoid FlexAttention recompiles when request counts change

</details>

<details>
<summary>MoE & quantization (13)</summary>

- [#53161](https://github.com/vllm-project/vllm/pull/53161) fuse native FP8 shared expert with MXFP4 routed experts (DSv4, ROCm)
- [#52263](https://github.com/vllm-project/vllm/pull/52263) AMD Quark per-block FP8 for fused MoE
- [#55890](https://github.com/vllm-project/vllm/pull/55890) tune FP8 TP2/TP4 Triton MoE on B200 for Qwen3.8-Flash-Next
- [#55511](https://github.com/vllm-project/vllm/pull/55511) fused MoE tuned config for E=256,N=512 on A100 PCIe
- [#55713](https://github.com/vllm-project/vllm/pull/55713) NVFP4 DSpark gathered top-k projection
- [#51925](https://github.com/vllm-project/vllm/pull/51925) FlashInfer add-RMSNorm NVFP4 fusion
- [#53319](https://github.com/vllm-project/vllm/pull/53319) NVFP4 support in torch linear backend
- [#52890](https://github.com/vllm-project/vllm/pull/52890) 2/3/5/6/7-bit CUDA support for AutoRound
- [#54890](https://github.com/vllm-project/vllm/pull/54890) FP8 indexer cache for QSA
- [#55377](https://github.com/vllm-project/vllm/pull/55377) autotune FlashInfer deferred MoE decode kernels before CUDA graph capture
- [#55407](https://github.com/vllm-project/vllm/pull/55407) fix Kimi K3 NVFP4 MoE weight conversion OOM
- [#53163](https://github.com/vllm-project/vllm/pull/53163) normalize unset group_size on compressed-tensors WNA16 MoE
- [#53586](https://github.com/vllm-project/vllm/pull/53586) DSv4 MXFP4 selector no longer narrows explicit aliases to BF16

</details>

<details>
<summary>Model support (12)</summary>

- [#56208](https://github.com/vllm-project/vllm/pull/56208) DeepSeek-V4.1-Flash in Rust and Python frontends
- [#54774](https://github.com/vllm-project/vllm/pull/54774) Cohere Compass model
- [#55921](https://github.com/vllm-project/vllm/pull/55921) Bailing V3 VL
- [#54371](https://github.com/vllm-project/vllm/pull/54371) Qwen4Exp UVA PLE-offload and Engram TP
- [#53614](https://github.com/vllm-project/vllm/pull/53614) Kimi K3 internal prefix checkpoints with partial prefix caching and spec decode
- [#55690](https://github.com/vllm-project/vllm/pull/55690) QKV-Fuser for Gemma4 in Transformers backend
- [#55301](https://github.com/vllm-project/vllm/pull/55301) generalize merged-column linear fusion in Transformers backend
- [#42785](https://github.com/vllm-project/vllm/pull/42785) encoder CUDA graph for MiniCPM-V
- [#53052](https://github.com/vllm-project/vllm/pull/53052) EAGLE3 for Sarvam
- [#55817](https://github.com/vllm-project/vllm/pull/55817) torch.compile for Sarvam MLA
- [#54574](https://github.com/vllm-project/vllm/pull/54574) MTP with separate quantized lm head for Nemotron
- [#53689](https://github.com/vllm-project/vllm/pull/53689) LoRA for DeepSeek V4 on XPU

</details>

<details>
<summary>Parallelism & scheduling (10)</summary>

- [#41567](https://github.com/vllm-project/vllm/pull/41567) ECMooncakeConnector for encoder cache over Mooncake TransferEngine
- [#53780](https://github.com/vllm-project/vllm/pull/53780) NIXL per-region transfer geometry
- [#52615](https://github.com/vllm-project/vllm/pull/52615) rename KV offload block to chunk
- [#54033](https://github.com/vllm-project/vllm/pull/54033) backend extension points for ECCPUWorker
- [#53903](https://github.com/vllm-project/vllm/pull/53903) report replicated-PCP ranks as done sending in NIXL
- [#54853](https://github.com/vllm-project/vllm/pull/54853) resolve connector block tables for every scheduled request
- [#55760](https://github.com/vllm-project/vllm/pull/55760) default prefix_cache_retention_interval to dense for Mamba + EAGLE
- [#53007](https://github.com/vllm-project/vllm/pull/53007) let SWA layers use the primary block size to avoid inflating KV block LCM
- [#52957](https://github.com/vllm-project/vllm/pull/52957) sync DP state on first step of a wave
- [#53491](https://github.com/vllm-project/vllm/pull/53491) extend CPU<->GPU sync checking to paged async copies

</details>

<details>
<summary>Hardware & arch (10)</summary>

- [#54787](https://github.com/vllm-project/vllm/pull/54787) fused allreduce+GemmaRMSNorm on ROCm for M3
- [#55099](https://github.com/vllm-project/vllm/pull/55099) ROCm multi-stream perf and rocprofiler fixes
- [#53195](https://github.com/vllm-project/vllm/pull/53195) enable WideEP intranode tests on ROCm
- [#54640](https://github.com/vllm-project/vllm/pull/54640) public CUDA 13.4 Rubin build path
- [#52945](https://github.com/vllm-project/vllm/pull/52945) fused_input_norm kernel on XPU
- [#53580](https://github.com/vllm-project/vllm/pull/53580) route grouped_topk to fused _moe_C kernel on XPU
- [#54405](https://github.com/vllm-project/vllm/pull/54405) enable HY-V4 init on ROCm
- [#55236](https://github.com/vllm-project/vllm/pull/55236) better KV dtype error discoverability on ROCm
- [#55942](https://github.com/vllm-project/vllm/pull/55942) forward_xpu for Ernie4_5_VL rotary embedding
- [#56014](https://github.com/vllm-project/vllm/pull/56014) update triton-xpu 3.8.0 shim

</details>

<details>
<summary>API & serving (14)</summary>

- [#54053](https://github.com/vllm-project/vllm/pull/54053) watermarked generation and detection (Gumbel-max)
- [#50195](https://github.com/vllm-project/vllm/pull/50195) stateless /v1/responses/render endpoint
- [#55417](https://github.com/vllm-project/vllm/pull/55417) Rust frontend whitespace framing in model output
- [#56174](https://github.com/vllm-project/vllm/pull/56174) strongly typed wire dtypes and modalities in Rust frontend
- [#54659](https://github.com/vllm-project/vllm/pull/54659) expose multimodal metadata for disaggregated prefill
- [#56090](https://github.com/vllm-project/vllm/pull/56090) JSON arrays for EPD multimodal metadata
- [#55411](https://github.com/vllm-project/vllm/pull/55411) simplify Rust reasoning parser init
- [#56018](https://github.com/vllm-project/vllm/pull/56018) consistent Rust parser selection
- [#55328](https://github.com/vllm-project/vllm/pull/55328) optional --max-model-len for Rust render server
- [#56058](https://github.com/vllm-project/vllm/pull/56058) normalize HTTP method labels in Rust metrics
- [#55735](https://github.com/vllm-project/vllm/pull/55735) migrate input validation errors to VLLMValidationError
- [#55701](https://github.com/vllm-project/vllm/pull/55701) migrate Responses harmony validation to VLLMValidationError
- [#50257](https://github.com/vllm-project/vllm/pull/50257) migrate Responses API validation errors
- [#55665](https://github.com/vllm-project/vllm/pull/55665) honor request_id from pooling request bodies

</details>

<details>
<summary>Bugfixes (50)</summary>

- [#53945](https://github.com/vllm-project/vllm/pull/53945) cache Mamba state at block-grid position on EAGLE resume
- [#54713](https://github.com/vllm-project/vllm/pull/54713) retain both replay boundaries for EAGLE resend
- [#55212](https://github.com/vllm-project/vllm/pull/55212) initialize DCP metadata after batch partitioning in MRV2
- [#55290](https://github.com/vllm-project/vllm/pull/55290) fail the request, not the engine, on missing remote encoding
- [#54362](https://github.com/vllm-project/vllm/pull/54362) fix SWA store reachability during chunked prefill in KV offload
- [#55712](https://github.com/vllm-project/vllm/pull/55712) validate SWA coverage at unaligned KV offload hit boundaries
- [#54756](https://github.com/vllm-project/vllm/pull/54756) register mixed page sizes in one KV offload cache group
- [#52771](https://github.com/vllm-project/vllm/pull/52771) OffloadingConnector no longer zeroes hits under MTP/EAGLE
- [#54288](https://github.com/vllm-project/vllm/pull/54288) stop offloading final sampled token's KV slot
- [#54998](https://github.com/vllm-project/vllm/pull/54998) respect prefix-cache bypass in SimpleCPUOffload
- [#55075](https://github.com/vllm-project/vllm/pull/55075) skip cleaned-up async lookup batches in KV offload
- [#54917](https://github.com/vllm-project/vllm/pull/54917) conditional KV projections/norms on Gemma KV-shared layers
- [#56141](https://github.com/vllm-project/vllm/pull/56141) tolerate misspelled DSML tool_calls wrapper
- [#55954](https://github.com/vllm-project/vllm/pull/55954) parse DSML tool calls when wrapper omitted
- [#53856](https://github.com/vllm-project/vllm/pull/53856) mask paged attention V cache padding on ROCm
- [#55887](https://github.com/vllm-project/vllm/pull/55887) shared KV prefill in AITER attention
- [#52516](https://github.com/vllm-project/vllm/pull/52516) Mooncake heterogeneous TP with replicated GQA heads
- [#52156](https://github.com/vllm-project/vllm/pull/52156) apply attention sinks in Transformers backend
- [#55213](https://github.com/vllm-project/vllm/pull/55213) fix AITER MXFP4 ASM-GEMM crash on unfused shared experts
- [#55643](https://github.com/vllm-project/vllm/pull/55643) fix NVFP4 fused SiLU+mul scale allocation and global scale direction
- [#55031](https://github.com/vllm-project/vllm/pull/55031) speed up NVFP4 KV for FMHA
- [#55513](https://github.com/vllm-project/vllm/pull/55513) block FP8 MTP in ModelOpt mixed checkpoints
- [#54788](https://github.com/vllm-project/vllm/pull/54788) honor draft's moe_backend on MRV2
- [#55369](https://github.com/vllm-project/vllm/pull/55369) resolve n_predict from text_config for Qwen3.5 multimodal MTP
- [#55472](https://github.com/vllm-project/vllm/pull/55472) preserve target DCP config for DSpark
- [#55458](https://github.com/vllm-project/vllm/pull/55458) exclude DP token padding from draft attention metadata
- [#55745](https://github.com/vllm-project/vllm/pull/55745) record_stream idx_mapping in PP draft broadcast
- [#55455](https://github.com/vllm-project/vllm/pull/55455) defer adaptive verification until after kernel warmup
- [#53379](https://github.com/vllm-project/vllm/pull/53379) Kimi K3 loading with interleaved weight streams
- [#55747](https://github.com/vllm-project/vllm/pull/55747) Kimi K3 checkpoint_idx assertion
- [#55774](https://github.com/vllm-project/vllm/pull/55774) Kimi K3 startup CUDA graph issue with recoverSSM
- [#53664](https://github.com/vllm-project/vllm/pull/53664) pipeline parallel for Kimi-K3 DCP on ROCm
- [#55861](https://github.com/vllm-project/vllm/pull/55861) apply dense prefix cache default to hybrid models
- [#55863](https://github.com/vllm-project/vllm/pull/55863) remove misleading Mamba prefix cache warning
- [#55461](https://github.com/vllm-project/vllm/pull/55461) fall back to T1 when ARC can't reclaim from T2
- [#55772](https://github.com/vllm-project/vllm/pull/55772) route only to surviving engines in Elastic EP scale-down
- [#54975](https://github.com/vllm-project/vllm/pull/54975) preserve prefetch static-buffer slot ownership in offloader
- [#54643](https://github.com/vllm-project/vllm/pull/54643) MooncakeStore finish-time save crash on hybrid models
- [#40416](https://github.com/vllm-project/vllm/pull/40416) ECExampleConnector load device under TP>1
- [#53174](https://github.com/vllm-project/vllm/pull/53174) Step-3.5 reasoning parser for structured outputs
- [#54264](https://github.com/vllm-project/vllm/pull/54264) Seed-OSS turn-boundary tokens
- [#55240](https://github.com/vllm-project/vllm/pull/55240) skip undefined token ids in Rust decode
- [#54022](https://github.com/vllm-project/vllm/pull/54022) gracefully handle unsupported reasoning_effort
- [#53824](https://github.com/vllm-project/vllm/pull/53824) detect OpenAI content format via macro parameters
- [#55307](https://github.com/vllm-project/vllm/pull/55307) honor STEP token pooling in DispatchPooler
- [#55941](https://github.com/vllm-project/vllm/pull/55941) OpenPangu multimodal embedding merge
- [#55949](https://github.com/vllm-project/vllm/pull/55949) handle null RoPE parameters for NoPE layers
- [#52651](https://github.com/vllm-project/vllm/pull/52651) XPU moe_wna16 linear weight loading
- [#56035](https://github.com/vllm-project/vllm/pull/56035) skip launch_pdl JIT warmup when PDL unsupported on ROCm
- plus 10 more minor bugfixes (audio decoding, Responses 400 vs 500, translation file validation, Molmo2, LoRA logging, XPU FalconH1 PP, others)

</details>

<details>
<summary>Refactors (4)</summary>

- [#55535](https://github.com/vllm-project/vllm/pull/55535) remove unused kernel fake implementations
- [#53941](https://github.com/vllm-project/vllm/pull/53941) remove utils dead code
- [#56103](https://github.com/vllm-project/vllm/pull/56103) extract maybe_run_omni() and defer CLI imports
- [#56078](https://github.com/vllm-project/vllm/pull/56078) unify XD-RoPE into M-RoPE

</details>

<details>
<summary>Tests (13)</summary>

- [#54973](https://github.com/vllm-project/vllm/pull/54973) e2e test for scale-out EC connector flow
- [#55889](https://github.com/vllm-project/vllm/pull/55889) reuse ColQwen3 models across pooling tests
- [#55797](https://github.com/vllm-project/vllm/pull/55797) fix unused fake implementation testing
- [#55908](https://github.com/vllm-project/vllm/pull/55908) dequantize NVFP4 KV scales in kernel layout for tests
- [#51450](https://github.com/vllm-project/vllm/pull/51450) keep invalid structured-output requests from stopping the engine
- [#51898](https://github.com/vllm-project/vllm/pull/51898) validate scale-out multimodal data before engine handoff
- [#55606](https://github.com/vllm-project/vllm/pull/55606) validate extension integers before engine serialization
- [#53590](https://github.com/vllm-project/vllm/pull/53590) fix ROCm AITER FP8 KV test tolerances
- [#55272](https://github.com/vllm-project/vllm/pull/55272) remove torch.compile for Qwen3.8-Flash-Next on NVIDIA
- [#56106](https://github.com/vllm-project/vllm/pull/56106) fix MoE layer tests for fp8 on ROCm
- [#56130](https://github.com/vllm-project/vllm/pull/56130) platform-independent GEMM in merged-column fuser test
- [#56010](https://github.com/vllm-project/vllm/pull/56010) reject CUDA-IPC weight cache on non-CUDA/ROCm platforms
- plus 6 more minor test fixes and skips (XPU, ROCm, ColQwen3)

</details>

<details>
<summary>CI & build (13)</summary>

- [#52346](https://github.com/vllm-project/vllm/pull/52346) split long misc test groups by command
- [#55163](https://github.com/vllm-project/vllm/pull/55163) upload CPU nightly image to Docker Hub
- [#55454](https://github.com/vllm-project/vllm/pull/55454) recover empty multi-node Docker networks
- [#53885](https://github.com/vllm-project/vllm/pull/53885) add GLM-5.2-FP8 to MoRIIO catalog
- [#53602](https://github.com/vllm-project/vllm/pull/53602) split MI300 distributed compile by graph partition mode
- [#55376](https://github.com/vllm-project/vllm/pull/55376) remove obsolete TPU Dockerfile
- [#54112](https://github.com/vllm-project/vllm/pull/54112) upgrade default AINIC repo for libionic
- [#55877](https://github.com/vllm-project/vllm/pull/55877) fix ARM64 dependency builds with GCC 15
- [#55529](https://github.com/vllm-project/vllm/pull/55529) add RL code owner
- [#55919](https://github.com/vllm-project/vllm/pull/55919) increase MI300 job timeouts
- [#56179](https://github.com/vllm-project/vllm/pull/56179) disable MRV2 for some XPU quantization tests
- [#55630](https://github.com/vllm-project/vllm/pull/55630) fix pre-commit
- plus 2 more minor CI updates

</details>

<details>
<summary>Docs (5)</summary>

- [#54522](https://github.com/vllm-project/vllm/pull/54522) CPU EC Connector usage docs
- [#55476](https://github.com/vllm-project/vllm/pull/55476) clarify security reporter credit and CVE timing
- [#55124](https://github.com/vllm-project/vllm/pull/55124) admission control limits apply server-wide
- [#51646](https://github.com/vllm-project/vllm/pull/51646) sync KV event medium terminology
- [#54584](https://github.com/vllm-project/vllm/pull/54584) MkDocs dev-server port option

</details>

<details>
<summary>Other (5)</summary>

- [#47505](https://github.com/vllm-project/vllm/pull/47505) guard lmcache_mp_connector state transition
- [#54523](https://github.com/vllm-project/vllm/pull/54523) scope PCP-DP validation to GPU manager
- [#55865](https://github.com/vllm-project/vllm/pull/55865) clarify LoRA target module matching
- [#56146](https://github.com/vllm-project/vllm/pull/56146) bound Cohere request priorities to int64
- plus 3 more minor changes

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (vllm.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 3c002441803dac144924a1e5a78e8024c9a2a0b73e30c0ad9d8eb29554070b49 -->
