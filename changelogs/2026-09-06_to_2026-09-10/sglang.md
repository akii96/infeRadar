# sglang: PR digest (2026-09-06 to 2026-09-10)

_230 merged, 442 newly opened - source sgl-project/sglang, generated 2026-09-10T13:56:14Z_

## TL;DR
- **DeepSeek (V4/V4.1) and GLM (5.2/5.3-Flash) got the most attention.** Merged work covers TRT-LLM DSv4 attention on SM100/103 (`[#30805](https://github.com/sgl-project/sglang/pull/30805)`), NPU arch35 for DSV4 (`[#37373](https://github.com/sgl-project/sglang/pull/37373)`), AMD unified-KV pool sizing (`[#38192](https://github.com/sgl-project/sglang/pull/38192)`), and GLM-5.3-Flash support (`[#36507](https://github.com/sgl-project/sglang/pull/36507)`). Open: DeepSeek V4.1 support (`[#38798](https://github.com/sgl-project/sglang/pull/38798)`), a direct INT4 KV cache for DSV4 (`[#38301](https://github.com/sgl-project/sglang/pull/38301)`), and a wave of AMD gfx950 GLM-5.3-Flash day-0 work.
- **Kernel and MoE work is the main performance story.** Merged: FlashInfer Mega MoE (`[#31470](https://github.com/sgl-project/sglang/pull/31470)`), the AMD Triton sparse-MLA backend (`[#30575](https://github.com/sgl-project/sglang/pull/30575)`), gfx950 assembly attention for EAGLE (`[#37465](https://github.com/sgl-project/sglang/pull/37465)`) and DSA top-k v2 (`[#38829](https://github.com/sgl-project/sglang/pull/38829)`). Open: NCCL EP Triton MoE (`[#38683](https://github.com/sgl-project/sglang/pull/38683)`, `[#38886](https://github.com/sgl-project/sglang/pull/38886)`, `[#38887](https://github.com/sgl-project/sglang/pull/38887)`, `[#38888](https://github.com/sgl-project/sglang/pull/38888)`) and a CUTLASS MXFP4xBF16 grouped GEMM for SM90 (`[#38884](https://github.com/sgl-project/sglang/pull/38884)`).
- **Qwen 3.8 Flash Next landed** (`[#37500](https://github.com/sgl-project/sglang/pull/37500)`), with follow-up SM120 and NVFP4 work open (MXFP4 KV `[#38724](https://github.com/sgl-project/sglang/pull/38724)`, RecoverSSM `[#38492](https://github.com/sgl-project/sglang/pull/38492)`).
- **Direction:** large cleanup, with context-parallel v1 and legacy kernels deleted (`[#32114](https://github.com/sgl-project/sglang/pull/32114)`, `[#38293](https://github.com/sgl-project/sglang/pull/38293)`, `[#36228](https://github.com/sgl-project/sglang/pull/36228)`), a staged config/ServerArgs refactor, test consolidation (`[#37436](https://github.com/sgl-project/sglang/pull/37436)`), and a Rust router/TreeCore push. In parallel, diffusion gained residency/offload infrastructure and MiniMax-H3 support.

## Most important PRs
**[#37500](https://github.com/sgl-project/sglang/pull/37500): support qwen 3.8 flash next**
Adds Qwen 3.8 Flash Next across attention, MoE, quantization, speculative decode and multimodal paths. It is the largest model-family feature merged this window, and NVFP4 recipes and MoE Triton configs for H200 followed.

**[#36507](https://github.com/sgl-project/sglang/pull/36507): GLM-5.3-Flash support**
Adds model support spanning MLA/DSA attention, MoE, quantization and speculative decode, with NPU and NVIDIA coverage. Several open PRs fix and extend it (HiCache restore corruption `[#38212](https://github.com/sgl-project/sglang/pull/38212)`, breakable prefill graphs `[#38522](https://github.com/sgl-project/sglang/pull/38522)`).

**[#31470](https://github.com/sgl-project/sglang/pull/31470): [NVIDIA] Support flashinfer Mega Moe**
Integrates FlashInfer's fused Mega MoE kernel with quantization and LoRA hooks. This gives a new fused MoE path on Blackwell.

**[#30805](https://github.com/sgl-project/sglang/pull/30805): [DSv4] Integrate TRT-LLM DSv4 Attention for SM100/103**
Hooks TRT-LLM's DeepSeek-V4 attention into the speculative-decode path on Blackwell, replacing a slower generic path.

**[#30575](https://github.com/sgl-project/sglang/pull/30575): [AMD] Enable Fast Triton Sparse MLA backend**
Adds a Triton sparse-MLA kernel backend for AMD DSA models. A gfx950 prefill/decode follow-up is open (`[#38601](https://github.com/sgl-project/sglang/pull/38601)`).

## More changes by area

<details>
<summary>Performance (9)</summary>

- [#37926](https://github.com/sgl-project/sglang/pull/37926) close the DCP decode gap for unified memory on Blackwell
- [#32911](https://github.com/sgl-project/sglang/pull/32911) add HRRN schedule policy to reduce TTFT
- [#37562](https://github.com/sgl-project/sglang/pull/37562) reduce `all_reduce` calls in HiCache event checks under PP
- [#38117](https://github.com/sgl-project/sglang/pull/38117) use the Gumbel-max trick in the sampler to cut decode CPU dispatch
- [#36143](https://github.com/sgl-project/sglang/pull/36143) use fp32 in TRTLLM all-reduce buffers
- [#38335](https://github.com/sgl-project/sglang/pull/38335) baseline e2e of ten unguarded diffusion perf cases
- [#38457](https://github.com/sgl-project/sglang/pull/38457) per-case timing tolerance for host-I/O-bound perf guards
- [#38629](https://github.com/sgl-project/sglang/pull/38629) don't fail the nightly on an unreadable perf dump
- [#34722](https://github.com/sgl-project/sglang/pull/34722) optimize LTX-2/2.3 inference on NPU

</details>

<details>
<summary>Kernels & attention (14)</summary>

- [#37591](https://github.com/sgl-project/sglang/pull/37591) make the ROCm DSA indexer top-k exact with cooperative selection
- [#37659](https://github.com/sgl-project/sglang/pull/37659) parallelize aiter spec-decode KV index building
- [#37601](https://github.com/sgl-project/sglang/pull/37601) qlen>1 for the aiter gluon path (Kimi K3)
- [#37691](https://github.com/sgl-project/sglang/pull/37691) aiter FA MHA chunked KV for Kimi K3
- [#37124](https://github.com/sgl-project/sglang/pull/37124) fused DSA metadata kernels on ROCm
- [#36527](https://github.com/sgl-project/sglang/pull/36527) MiniMax-M3 shares sparse index top-k across layers
- [#36557](https://github.com/sgl-project/sglang/pull/36557) MiniMax-M3 Triton split-K router GEMV
- [#38124](https://github.com/sgl-project/sglang/pull/38124) drop the vendored BF16 GEMM for FlashInfer 0.6.18
- [#38182](https://github.com/sgl-project/sglang/pull/38182) Wan VAE channels_last plus a Triton NHWC upsample
- [#38396](https://github.com/sgl-project/sglang/pull/38396) optimize LTX-2 QKNorm and split RoPE on Hopper
- [#38530](https://github.com/sgl-project/sglang/pull/38530) fuse LongCat Image normalization and modulation
- [#37982](https://github.com/sgl-project/sglang/pull/37982) SM90 Sage compute for MiniMax-H3 SubBlock sparse attention
- [#38290](https://github.com/sgl-project/sglang/pull/38290) wait for the PDL dependency before loading the router bias
- [#38399](https://github.com/sgl-project/sglang/pull/38399) bench: amortize GDN ReplaySSM decode latency

</details>

<details>
<summary>MoE & quantization (11)</summary>

- [#38830](https://github.com/sgl-project/sglang/pull/38830) port expert-pack MXFP4 kernels to load_jit and fix launch limits
- [#38116](https://github.com/sgl-project/sglang/pull/38116) fused MoE Triton configs for Qwen3.8-Flash-Next FP8 on H200 NVL
- [#30430](https://github.com/sgl-project/sglang/pull/30430) fuse Nemotron latent MoE projection and shared add
- [#33631](https://github.com/sgl-project/sglang/pull/33631) keep fp32 routing weights in the fp8 block-scale and bf16 trtllm MoE
- [#33608](https://github.com/sgl-project/sglang/pull/33608) keep fp32 routing weights in the DSv4 mxfp4 trtllm MoE
- [#33591](https://github.com/sgl-project/sglang/pull/33591) drop routing bias casts in the flashinfer trtllm MoE
- [#38612](https://github.com/sgl-project/sglang/pull/38612) accept fp32 routing weights in Kimi-K3 fused MoE finalize
- [#37133](https://github.com/sgl-project/sglang/pull/37133) keep GlmMoeDsa e_score_correction_bias in fp32 on AMD
- [#37325](https://github.com/sgl-project/sglang/pull/37325) disable Hopper GLM shared-expert fusion for modelopt_fp4 Marlin
- [#37376](https://github.com/sgl-project/sglang/pull/37376) add fused silu-mul-quant fp8 (reverted by [#38381](https://github.com/sgl-project/sglang/pull/38381))
- [#38881](https://github.com/sgl-project/sglang/pull/38881) drop the GPTQ dynamic-config test for the deleted non-Marlin kernel

</details>

<details>
<summary>Model support (13)</summary>

- [#36606](https://github.com/sgl-project/sglang/pull/36606) SenseNova-U1.5-8B-MoT diffusion support
- [#38621](https://github.com/sgl-project/sglang/pull/38621) GLM-5.3 Flash NVFP4 loading
- [#38250](https://github.com/sgl-project/sglang/pull/38250) NPU GLM-5.2 and FP8 DSA/indexer KV cache for 950
- [#24959](https://github.com/sgl-project/sglang/pull/24959) GLM5.1 DSA attention on XPU
- [#38455](https://github.com/sgl-project/sglang/pull/38455) MiniMax-H3 Singularity hybrid checkpoints
- [#33366](https://github.com/sgl-project/sglang/pull/33366) MiniMax-H3 on XPU
- [#35147](https://github.com/sgl-project/sglang/pull/35147) MiniMax-H3 on Xeon CPU
- [#38506](https://github.com/sgl-project/sglang/pull/38506) mixed INT8 embeddings and Comfy NVFP4 encoders (diffusion)
- [#36026](https://github.com/sgl-project/sglang/pull/36026) decoder parallel tiling for LTX-2.5
- [#38591](https://github.com/sgl-project/sglang/pull/38591) lossless BCG for FLUX.1-dev
- [#38434](https://github.com/sgl-project/sglang/pull/38434) Ling-3.0-flash-VL cookbook
- [#38527](https://github.com/sgl-project/sglang/pull/38527) INT4/FP4 lanes in the Ling cookbook
- plus 4 more cookbook/doc PRs (MiniCPM5-2B `[#38295](https://github.com/sgl-project/sglang/pull/38295)`, DeepSeek-V4.1 Flash `[#38802](https://github.com/sgl-project/sglang/pull/38802)`, `[#38844](https://github.com/sgl-project/sglang/pull/38844)`, Qwen3.8 NVFP4 `[#37995](https://github.com/sgl-project/sglang/pull/37995)`)

</details>

<details>
<summary>Parallelism & scheduling (15)</summary>

- [#38108](https://github.com/sgl-project/sglang/pull/38108) router bucket-aware policy domains and native cache indexing
- [#38139](https://github.com/sgl-project/sglang/pull/38139) router publishes cache-aware load state
- [#36848](https://github.com/sgl-project/sglang/pull/36848) HiCache segment lock protocol replaces skip_lock_node_ids
- [#36800](https://github.com/sgl-project/sglang/pull/36800) HiCache MLA host-dedup primitives
- [#36713](https://github.com/sgl-project/sglang/pull/36713) evict Full KV for Mamba byte shortfalls in unified memory
- [#38159](https://github.com/sgl-project/sglang/pull/38159) free hybrid SWA pages per representative on page_size>1
- [#34820](https://github.com/sgl-project/sglang/pull/34820) store mamba prefix-cache checkpoints at the configured SSM dtype
- [#36899](https://github.com/sgl-project/sglang/pull/36899) optimized Domino rollout for DFlash V2
- [#37143](https://github.com/sgl-project/sglang/pull/37143) rank-consistent request-timeout aborts to fix TP collective hangs
- [#38389](https://github.com/sgl-project/sglang/pull/38389) unify request intake into ingest_requests()
- [#37306](https://github.com/sgl-project/sglang/pull/37306) Rust TreeCore external cache linker
- [#37303](https://github.com/sgl-project/sglang/pull/37303) Rust TreeCore runtime and CI hardening
- [#38165](https://github.com/sgl-project/sglang/pull/38165) publish fresh streamed LoRA versions alongside generation
- [#36988](https://github.com/sgl-project/sglang/pull/36988) retire aborted disaggregated prefill results (VLM)
- [#32207](https://github.com/sgl-project/sglang/pull/32207) NPU EAGLE with PP in prefill nodes

</details>

<details>
<summary>Hardware & arch (19)</summary>

- [#37373](https://github.com/sgl-project/sglang/pull/37373) NPU arch35 and DSV4 processing
- [#33089](https://github.com/sgl-project/sglang/pull/33089) NPU sparsity-driven KV offload for DeepSeek DSA
- [#35629](https://github.com/sgl-project/sglang/pull/35629) DFlash2 speculative decoding on Ascend
- [#32495](https://github.com/sgl-project/sglang/pull/32495) NPU non-greedy MTP sampling
- [#38174](https://github.com/sgl-project/sglang/pull/38174) NPU mf device urma and host rdma transfer types
- [#37758](https://github.com/sgl-project/sglang/pull/37758) NPU ViT graph key layout fix
- [#38249](https://github.com/sgl-project/sglang/pull/38249) NPU PP=2 hang fix
- [#38112](https://github.com/sgl-project/sglang/pull/38112) NPU test fixes and efficiency
- [#38437](https://github.com/sgl-project/sglang/pull/38437) NPU memfabric/sgl-kernel-npu version bumps
- [#38667](https://github.com/sgl-project/sglang/pull/38667) NPU DEEPEP_HYBRID_DEPLOYMENT for collocated DeepEP tests
- [#37465](https://github.com/sgl-project/sglang/pull/37465) gfx950 assembly attention for EAGLE
- [#37140](https://github.com/sgl-project/sglang/pull/37140) hardware fp8 e4m3 convert on gfx950
- [#38467](https://github.com/sgl-project/sglang/pull/38467) skip AITER FP8 ASM prefill when GQA is unsupported
- [#38192](https://github.com/sgl-project/sglang/pull/38192) AMD DSV4 unified-KV pool reland (after revert [#38163](https://github.com/sgl-project/sglang/pull/38163))
- [#38571](https://github.com/sgl-project/sglang/pull/38571) AMD DSV4 skip paged SWA page return under per-request ring
- [#30345](https://github.com/sgl-project/sglang/pull/30345) LoRA on Intel XPU
- [#35866](https://github.com/sgl-project/sglang/pull/35866) MLA prefill in the Intel XPU attention backend
- [#31113](https://github.com/sgl-project/sglang/pull/31113) NUMA binding for Intel XPU
- plus 3 more XPU/MUSA/CPU items (`[#29935](https://github.com/sgl-project/sglang/pull/29935)`, `[#36709](https://github.com/sgl-project/sglang/pull/36709)`, `[#35604](https://github.com/sgl-project/sglang/pull/35604)`)

</details>

<details>
<summary>API & serving (4)</summary>

- [#37994](https://github.com/sgl-project/sglang/pull/37994) gate Rust server health on startup warmup
- [#34430](https://github.com/sgl-project/sglang/pull/34430) node-local HTTP ports for DP attention in the Rust server
- [#31415](https://github.com/sgl-project/sglang/pull/31415) Ray metric backend for engine metrics
- [#38279](https://github.com/sgl-project/sglang/pull/38279) allow sampling-mask replay with DisallowedTokensLogitsProcessor

</details>

<details>
<summary>Bugfixes (22)</summary>

- [#36944](https://github.com/sgl-project/sglang/pull/36944) contain EPD request lifecycle failures
- [#33922](https://github.com/sgl-project/sglang/pull/33922) Qwen3.5 GDN multi-item scoring
- [#36298](https://github.com/sgl-project/sglang/pull/36298) Whisper XPU varlen encoder-decoder
- [#35051](https://github.com/sgl-project/sglang/pull/35051) pack device-pointer tables as uint64 on XPU
- [#32758](https://github.com/sgl-project/sglang/pull/32758) bound Mooncake sync transfer batches (GLM-5.2 NVFP4)
- [#37199](https://github.com/sgl-project/sglang/pull/37199) avoid duplicate MoE reduction for gpt-oss with DP attention
- [#37933](https://github.com/sgl-project/sglang/pull/37933) keep a shared MAX_LEN prefill graph bucket for MegaMoE DP gather
- [#34919](https://github.com/sgl-project/sglang/pull/34919) DSpark CUDA graph replay with MegaMoE TP attention
- [#34459](https://github.com/sgl-project/sglang/pull/34459) DeepSeek-V4 routing sqrtsoftplus underflow
- [#37093](https://github.com/sgl-project/sglang/pull/37093) bound DSA prefill Triton specializations
- [#38564](https://github.com/sgl-project/sglang/pull/38564) stamp sequence-parallel state on dummy forward batches
- [#38590](https://github.com/sgl-project/sglang/pull/38590) size FlashInfer MLA indptr buffers to padded max batch
- [#38318](https://github.com/sgl-project/sglang/pull/38318) AMD EAGLE crash without kv_index_translator
- [#37165](https://github.com/sgl-project/sglang/pull/37165) clear deferred Mamba init metadata before spec decode
- [#37743](https://github.com/sgl-project/sglang/pull/37743) Kimi-K3 recover reply when the think channel is skipped
- [#38138](https://github.com/sgl-project/sglang/pull/38138) preserve SWA host lock on node split
- [#38313](https://github.com/sgl-project/sglang/pull/38313) and [#38204](https://github.com/sgl-project/sglang/pull/38204) iterative DFS/hash traversal to avoid recursion
- [#38171](https://github.com/sgl-project/sglang/pull/38171) restore non-layer placeholders before releasing host copies
- [#34142](https://github.com/sgl-project/sglang/pull/34142) fix inflated CP round-robin row pitch
- [#37789](https://github.com/sgl-project/sglang/pull/37789) fix missing latency span attributes
- [#37179](https://github.com/sgl-project/sglang/pull/37179) CPU shm allreduce collision fix
- [#38839](https://github.com/sgl-project/sglang/pull/38839) fix the DeepSeek-V4.1 reasoning example

</details>

<details>
<summary>Refactors (14)</summary>

- [#37436](https://github.com/sgl-project/sglang/pull/37436) consolidate test cleanup and CI taxonomy (net -11.4K lines)
- [#32114](https://github.com/sgl-project/sglang/pull/32114) delete cutlass_mla, non-Marlin GPTQ, AWQ AOT, Dual Chunk Flash Attention
- [#38293](https://github.com/sgl-project/sglang/pull/38293) deprecate HIP/NPU/MUSA prefill CP v1
- [#36228](https://github.com/sgl-project/sglang/pull/36228) remove generic prefill CP v1 runtime
- [#36229](https://github.com/sgl-project/sglang/pull/36229) canonicalize prefill CP API names
- [#36230](https://github.com/sgl-project/sglang/pull/36230) update prefill CP docs
- [#38375](https://github.com/sgl-project/sglang/pull/38375) retire get_global_server_args
- [#38753](https://github.com/sgl-project/sglang/pull/38753) msgspec.Struct for the config tier
- [#38752](https://github.com/sgl-project/sglang/pull/38752) single writer for the declaration stash
- [#38113](https://github.com/sgl-project/sglang/pull/38113), [#38049](https://github.com/sgl-project/sglang/pull/38049), [#38048](https://github.com/sgl-project/sglang/pull/38048), [#38046](https://github.com/sgl-project/sglang/pull/38046), [#38047](https://github.com/sgl-project/sglang/pull/38047) config rounds 6.1 to 6.5
- [#38699](https://github.com/sgl-project/sglang/pull/38699) diffusion utility ownership refactor
- [#38128](https://github.com/sgl-project/sglang/pull/38128) and [#38127](https://github.com/sgl-project/sglang/pull/38127) consolidated plain state-dict loaders (diffusion)
- [#38095](https://github.com/sgl-project/sglang/pull/38095) remove opaque type in sglang-server
- [#37886](https://github.com/sgl-project/sglang/pull/37886) remove obsolete CUDA graph buffer population methods

</details>

<details>
<summary>Diffusion features (7)</summary>

- [#37916](https://github.com/sgl-project/sglang/pull/37916) warmup memory and per-phase layer usage for residency calibration
- [#38441](https://github.com/sgl-project/sglang/pull/38441) stream mapped weights on a shared host/device pool
- [#38535](https://github.com/sgl-project/sglang/pull/38535) explicit snapshot-offload component residency
- [#38656](https://github.com/sgl-project/sglang/pull/38656) spill large tensors over shared memory
- [#38496](https://github.com/sgl-project/sglang/pull/38496) key the VAE decode-dtype store by module layout
- [#37350](https://github.com/sgl-project/sglang/pull/37350) reuse disk LoRA mapping on H3 IPC updates
- [#38226](https://github.com/sgl-project/sglang/pull/38226) quiet internal warmup frame searches

</details>

<details>
<summary>Tests (14)</summary>

- [#38185](https://github.com/sgl-project/sglang/pull/38185) validate every repeated diffusion server request
- [#38172](https://github.com/sgl-project/sglang/pull/38172) guard allocated VRAM peak in diffusion CI
- [#38336](https://github.com/sgl-project/sglang/pull/38336) offline Transformers loader compatibility checks
- [#38259](https://github.com/sgl-project/sglang/pull/38259) drop stale aiter gluon fp8 test
- [#38288](https://github.com/sgl-project/sglang/pull/38288) remove obsolete split-dim check from Kimi-K3 prefill test
- [#38372](https://github.com/sgl-project/sglang/pull/38372), [#38280](https://github.com/sgl-project/sglang/pull/38280) remove stale CP mocks
- [#38315](https://github.com/sgl-project/sglang/pull/38315) fix stale ServerArgs fake in chunked-SGMV LoRA test
- [#38314](https://github.com/sgl-project/sglang/pull/38314) fix DSpark dp-tier fixture
- [#38342](https://github.com/sgl-project/sglang/pull/38342) fix EP scale joiner test patch
- [#38732](https://github.com/sgl-project/sglang/pull/38732) simulator tolerance headroom
- [#38244](https://github.com/sgl-project/sglang/pull/38244) CustomTestCase for CPU tests
- [#38581](https://github.com/sgl-project/sglang/pull/38581) restore AMD CI registrations
- [#38225](https://github.com/sgl-project/sglang/pull/38225) stabilize H3 reference audio across requests
- [#38686](https://github.com/sgl-project/sglang/pull/38686) AMD diffusion perf fixture lookup

</details>

<details>
<summary>CI & build (16)</summary>

- [#38238](https://github.com/sgl-project/sglang/pull/38238) update CI test est_time values
- [#38380](https://github.com/sgl-project/sglang/pull/38380) replace Lark queue-digest card with a queue-timeline chart
- [#38734](https://github.com/sgl-project/sglang/pull/38734) /run-full-ci and /run-extra-ci slash commands
- [#38736](https://github.com/sgl-project/sglang/pull/38736) answer unrecognized slash commands
- [#38770](https://github.com/sgl-project/sglang/pull/38770) temporarily disable GB300 tests (reverted by [#38842](https://github.com/sgl-project/sglang/pull/38842))
- [#38763](https://github.com/sgl-project/sglang/pull/38763) publish ROCm 10 release images and kernel wheel
- [#38659](https://github.com/sgl-project/sglang/pull/38659) ROCm 10 default for AMD PR/nightly
- [#38694](https://github.com/sgl-project/sglang/pull/38694) drop miles ROCm 7.0 nightly image
- [#37495](https://github.com/sgl-project/sglang/pull/37495) move miles nightlies to rocm10
- [#37784](https://github.com/sgl-project/sglang/pull/37784) update ROCm AITER pin
- [#38456](https://github.com/sgl-project/sglang/pull/38456) copy MoE weight views before H2D in AMD slow-loading nightlies
- [#38239](https://github.com/sgl-project/sglang/pull/38239) rebalance diffusion 2-GPU shards
- [#37800](https://github.com/sgl-project/sglang/pull/37800) fix empty XPU nightly dashboard
- [#38014](https://github.com/sgl-project/sglang/pull/38014) merge XPU stage-a+b
- plus 4 more minor XPU docker/CI fixes (`[#38665](https://github.com/sgl-project/sglang/pull/38665)`, `[#38796](https://github.com/sgl-project/sglang/pull/38796)`, `[#38617](https://github.com/sgl-project/sglang/pull/38617)`, `[#33624](https://github.com/sgl-project/sglang/pull/33624)`)

</details>

<details>
<summary>Docs (5)</summary>

- [#38374](https://github.com/sgl-project/sglang/pull/38374) Qwen3.5 FP8 on B200/B300 cookbook
- [#38296](https://github.com/sgl-project/sglang/pull/38296) GB300/GB200 H3 recipes
- [#38534](https://github.com/sgl-project/sglang/pull/38534) JoyEcho H200 residency/BCG recipe
- [#38784](https://github.com/sgl-project/sglang/pull/38784) sync snapshot and MiniMax-H3 SubBlock features
- plus 3 more (`[#35674](https://github.com/sgl-project/sglang/pull/35674)`, `[#37456](https://github.com/sgl-project/sglang/pull/37456)`, `[#38148](https://github.com/sgl-project/sglang/pull/38148)`)

</details>

<details>
<summary>Other (10)</summary>

- [#38522](https://github.com/sgl-project/sglang/pull/38522) opt-in GLM-5.3 Flash breakable prefill CUDA graphs
- [#37767](https://github.com/sgl-project/sglang/pull/37767) allow fi_a2a on single-node Blackwell without MNNVL
- [#32759](https://github.com/sgl-project/sglang/pull/32759) AMD restore SWA reprefill-tail on UnifiedRadixCache
- [#38462](https://github.com/sgl-project/sglang/pull/38462) skip duplicate host evict via environ
- [#38735](https://github.com/sgl-project/sglang/pull/38735) raise router chat body cap to 32 MB
- [#38677](https://github.com/sgl-project/sglang/pull/38677) AMD v4 args for agentic workload
- [#38677](https://github.com/sgl-project/sglang/pull/38677) and [#38308](https://github.com/sgl-project/sglang/pull/38308) (qwen4 cherry-pick: avoid zero-bias allocation in fused softmax routing)
- [#38041](https://github.com/sgl-project/sglang/pull/38041) revert multi-layer EAGLE shared-read event
- [#38381](https://github.com/sgl-project/sglang/pull/38381) revert fused silu-mul-quant fp8
- [#38163](https://github.com/sgl-project/sglang/pull/38163) revert AMD DSV4 unified-KV pool sizing (relanded as `[#38192](https://github.com/sgl-project/sglang/pull/38192)`)

</details>

<details>
<summary>Newly opened (in progress, highlights)</summary>

- [#38798](https://github.com/sgl-project/sglang/pull/38798) DeepSeek V4.1 support
- [#38301](https://github.com/sgl-project/sglang/pull/38301) direct INT4 KV cache for DSV4 (+29% token capacity)
- [#38888](https://github.com/sgl-project/sglang/pull/38888), [#38887](https://github.com/sgl-project/sglang/pull/38887), [#38886](https://github.com/sgl-project/sglang/pull/38886), [#38683](https://github.com/sgl-project/sglang/pull/38683) NCCL EP Triton MoE stack
- [#38884](https://github.com/sgl-project/sglang/pull/38884) CUTLASS MXFP4xBF16 grouped GEMM MoE for SM90 (up to 20% long-context prefill gain)
- [#38344](https://github.com/sgl-project/sglang/pull/38344) prefill CP for linear attention (GDN/KDA)
- [#38326](https://github.com/sgl-project/sglang/pull/38326), [#38327](https://github.com/sgl-project/sglang/pull/38327) EAGLE3 and DSpark for MiniCPM-SALA
- [#38724](https://github.com/sgl-project/sglang/pull/38724) MXFP4 KV cache for Qwen3.5/3.8 on SM120
- [#38473](https://github.com/sgl-project/sglang/pull/38473), [#38468](https://github.com/sgl-project/sglang/pull/38468), [#38356](https://github.com/sgl-project/sglang/pull/38356) kv-shard stack
- [#38583](https://github.com/sgl-project/sglang/pull/38583), [#38546](https://github.com/sgl-project/sglang/pull/38546), [#38545](https://github.com/sgl-project/sglang/pull/38545), [#38547](https://github.com/sgl-project/sglang/pull/38547), [#38544](https://github.com/sgl-project/sglang/pull/38544) AMD gfx950 GLM-5.2/5.3-Flash work
- [#38901](https://github.com/sgl-project/sglang/pull/38901), [#38303](https://github.com/sgl-project/sglang/pull/38303) AMD DSV4 DSpark and FP4 LiteTopK indexer
- [#38632](https://github.com/sgl-project/sglang/pull/38632), [#38767](https://github.com/sgl-project/sglang/pull/38767) retire ROCm 7.0 CI
- [#38404](https://github.com/sgl-project/sglang/pull/38404), [#38641](https://github.com/sgl-project/sglang/pull/38641) retire CUDA 12 lane, upgrade to PyTorch 2.14

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (sglang.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 2eaf929d3ef5ee295bc93095e6e9faedf9c621cb7d8eb1a270d46d98387956a9 -->
