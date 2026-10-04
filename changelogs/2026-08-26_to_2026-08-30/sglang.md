# sglang: PR digest (2026-08-26 to 2026-08-30)

_295 merged, 390 newly opened - source sgl-project/sglang, generated 2026-08-30T23:44:47Z_

## TL;DR
- **Model focus:** DeepSeek (V4/DSA) and GLM (5.3-Flash) got the most label attention. MiniMax (M3/H3) and the Qwen 3.8 / Qwen3.5 family followed. Qwen 3.8 Flash Next, GLM-5.3-Flash and Hy4 are mostly large newly opened PRs, with cookbooks already merged.
- **Performance work:** DSV4 on AMD (MoRI MXFP8 dispatch, split-K retune, topk_transform v2) and a W4AFP8 DeepEP requant retune merged. Opened PRs add MXFP4 KV cache and a fused SM90 MXFP4 decode kernel for DSV4, plus a new SM100 sparse prefill. Diffusion fusions (Wan, Qwen-Image, FLUX.2 FP8/NVFP4 epilogues) are a steady stream.
- **Comms and memory:** The custom all-reduce was split into push/pull planes, and CUDA-graph prefill gained PP support and DP-attention coordination. Unified-memory and HiCache work continues across many small fixes.
- **Direction:** A large share of merged churn is a config-system refactor (resolution/ServerArgs/ReqKvInfo). It sits alongside a broad push to support new hardware (gfx1250, SM120, Rubin/CUDA 13.4, Apple MPS) and new models.

## Most important PRs
**[#35758](https://github.com/sgl-project/sglang/pull/35758) - qwen 3.8 rebase**
Merged rebase landing Qwen 3.8 across attention, MoE, quantization and spec-decode paths (~14.8k lines). It is the base for the Qwen 3.8 Flash Next and Max-VL PRs still open.

**[#35735](https://github.com/sgl-project/sglang/pull/35735) - Split custom all-reduce communicator into push/pull planes**
Restructures the custom all-reduce kernel path. Per its perf label, it targets lower collective latency and is the foundation for the NVLink collective and v2 dispatch rebuild work now open.

**[#35634](https://github.com/sgl-project/sglang/pull/35634) - DeepEPv2 (ElasticBuffer) MoE A2A backend**
Adds a new expert-parallel all-to-all backend, giving MoE serving another dispatch option alongside the existing DeepEP paths.

**[#31626](https://github.com/sgl-project/sglang/pull/31626) - Beam search support**
A long-running feature (144 commits) that adds beam search through the scheduler and speculative/structured-output paths.

**[#35314](https://github.com/sgl-project/sglang/pull/35314) - DeepSeek V4 and Kimi K3 on SSD**
Extends DSV4 and Kimi K3 serving to SSD-backed storage, covering MLA/MoE/quantization paths, so large checkpoints and KV can spill beyond memory.

## More changes by area

<details>
<summary>Performance (16)</summary>

- [#35760](https://github.com/sgl-project/sglang/pull/35760) tune W4AFP8 DeepEP low-latency requant launch geometry
- [#33871](https://github.com/sgl-project/sglang/pull/33871) reduce idle DP work in breakable prefill CUDA graphs
- [#36568](https://github.com/sgl-project/sglang/pull/36568) skip redundant scheduler metadata gather for DP1
- [#36705](https://github.com/sgl-project/sglang/pull/36705) stop populating HiCache host-pool mmaps twice (-13% alloc time)
- [#36397](https://github.com/sgl-project/sglang/pull/36397) tune custom all-reduce v2 for sm_107
- [#36119](https://github.com/sgl-project/sglang/pull/36119) AMD DSV4 MXFP8 MoRI dispatch to match the w4a8 MoE input
- [#36094](https://github.com/sgl-project/sglang/pull/36094) AMD DSV4 retune decode split-K heuristic for MI355X
- [#36130](https://github.com/sgl-project/sglang/pull/36130) AMD DSV4 bound the MoRI receive buffer in decode
- [#35275](https://github.com/sgl-project/sglang/pull/35275) reduce CUDA graph memory for adaptive speculative decoding
- [#36330](https://github.com/sgl-project/sglang/pull/36330) optimize Qwen3.5 MTP unified attention on gfx950
- [#34318](https://github.com/sgl-project/sglang/pull/34318) route large SM90 row/column-scaled FP8 GEMMs to Torch
- [#37070](https://github.com/sgl-project/sglang/pull/37070) scatter mm embeddings via index_copy_ to cut transient GPU memory
- [#36543](https://github.com/sgl-project/sglang/pull/36543) tune LingBot-Video MoE TMA configs for H100
- [#35374](https://github.com/sgl-project/sglang/pull/35374) H200 MoE configs for Qwen3.5/3.6
- [#35944](https://github.com/sgl-project/sglang/pull/35944) pin scheduler metadata before async H2D copies
- [#34599](https://github.com/sgl-project/sglang/pull/34599) optimize Pi0.5 inference and bounded graph serving
</details>

<details>
<summary>Kernels & attention (14)</summary>

- [#33576](https://github.com/sgl-project/sglang/pull/33576) AMD Work-Centric (Lean) Attention persistent-CTA decode kernel
- [#34446](https://github.com/sgl-project/sglang/pull/34446) fix fused Qwen3.5 RoPE dropping mrope height/width
- [#36003](https://github.com/sgl-project/sglang/pull/36003) skip reserved writes in MLA KV cache
- [#36758](https://github.com/sgl-project/sglang/pull/36758) AMD Qwen3.5 ASM FMHA chunked-prefill
- [#36356](https://github.com/sgl-project/sglang/pull/36356) aiter MLA asm path via head padding for Kimi K3
- [#36852](https://github.com/sgl-project/sglang/pull/36852) token-level KV indices in aiter ASM prefill gather
- [#35453](https://github.com/sgl-project/sglang/pull/35453) LSE on RadixAttention extra-kwargs graph path
- [#35434](https://github.com/sgl-project/sglang/pull/35434) CPU fix for wrongly causal-masked bidirectional attention
- [#36845](https://github.com/sgl-project/sglang/pull/36845) restore SM121 QSA correctness
- [#36806](https://github.com/sgl-project/sglang/pull/36806) route exact SM120 to FlashInfer sparse decode
- [#36684](https://github.com/sgl-project/sglang/pull/36684) enable DSV4 topk_transform v2 on AMD
- [#36313](https://github.com/sgl-project/sglang/pull/36313) add --speculative-dsa-topk-backend
- [#36521](https://github.com/sgl-project/sglang/pull/36521) avoid 4D scale-shift autotuning
- [#36502](https://github.com/sgl-project/sglang/pull/36502) fuse Helios paired transposed RoPE
</details>

<details>
<summary>MoE & quantization (7)</summary>

- [#32665](https://github.com/sgl-project/sglang/pull/32665) extension points for custom MoE runner backends
- [#29718](https://github.com/sgl-project/sglang/pull/29718) simulated expert routing with DP>1, fused into one Triton kernel
- [#36657](https://github.com/sgl-project/sglang/pull/36657) reserve SMs for DeepGEMM MegaMoE grid barriers
- [#36275](https://github.com/sgl-project/sglang/pull/36275) guard FP8 delegate activation params
- [#35883](https://github.com/sgl-project/sglang/pull/35883) fix stale GLM MoE routing after runtime weight updates
- [#35547](https://github.com/sgl-project/sglang/pull/35547) Laguna NVFP4 nightly gsm8k tests
- [#36396](https://github.com/sgl-project/sglang/pull/36396) AMD DSV4-Flash FP8 accuracy CI on MI30x
</details>

<details>
<summary>Model support (13)</summary>

- [#33561](https://github.com/sgl-project/sglang/pull/33561) Ling-3.0-flash (BailingMoeV3)
- [#34747](https://github.com/sgl-project/sglang/pull/34747) Cosmos3 transfer capability
- [#36607](https://github.com/sgl-project/sglang/pull/36607) enable GLM-5.3-Flash on gfx942/gfx950
- [#36708](https://github.com/sgl-project/sglang/pull/36708) DFLASH GLM-5.3-Flash hidden-state capture
- [#36755](https://github.com/sgl-project/sglang/pull/36755) fix DFLASH aux hidden-state capture on mHC models
- [#35947](https://github.com/sgl-project/sglang/pull/35947) gated DSV4 DFLASH target-prefill read completion
- [#35850](https://github.com/sgl-project/sglang/pull/35850) restrict MiniMax-H3 SubBlock sparsity to video queries
- [#36301](https://github.com/sgl-project/sglang/pull/36301) batching for cosmos3 action generation
- [#31320](https://github.com/sgl-project/sglang/pull/31320) NPU distributed pipeline for GLM-Image
- [#36827](https://github.com/sgl-project/sglang/pull/36827) GLM-5.3 cookbook
- [#36440](https://github.com/sgl-project/sglang/pull/36440) GLM-5.3-Flash cookbook
- [#36496](https://github.com/sgl-project/sglang/pull/36496) Qwen3.8-Flash-Next cookbook
- [#36804](https://github.com/sgl-project/sglang/pull/36804) Hy4-Preview cookbook page
</details>

<details>
<summary>Parallelism & scheduling (15)</summary>

- [#35451](https://github.com/sgl-project/sglang/pull/35451) PP support in full prefill CUDA graphs
- [#35640](https://github.com/sgl-project/sglang/pull/35640) coordinate FullCG prefill across DP-attention ranks
- [#35762](https://github.com/sgl-project/sglang/pull/35762) pack DCP1→DCP-N PD KV transfers into contiguous RDMA blocks
- [#36288](https://github.com/sgl-project/sglang/pull/36288) mixed chunk prefill base
- [#34608](https://github.com/sgl-project/sglang/pull/34608) publish per-scheduler load on a dedicated socket for routers
- [#35343](https://github.com/sgl-project/sglang/pull/35343) sync FlashInfer autotune tactic across TP ranks
- [#33614](https://github.com/sgl-project/sglang/pull/33614) fix Dspark/Dflash state divergence across TP ranks
- [#36160](https://github.com/sgl-project/sglang/pull/36160) align mori prefill transfer control plane
- [#36834](https://github.com/sgl-project/sglang/pull/36834) HiCache buffer-mode staged-fetch fate vs live tree
- [#36227](https://github.com/sgl-project/sglang/pull/36227) retry L3 prefetch after a miss
- [#36798](https://github.com/sgl-project/sglang/pull/36798) align chunked CUDA host registrations for HiCache
- [#35931](https://github.com/sgl-project/sglang/pull/35931) reject HiCache load-back specs on pinned nodes
- [#36317](https://github.com/sgl-project/sglang/pull/36317) keep auxiliary load-back out of Full KV pending ownership
- [#36382](https://github.com/sgl-project/sglang/pull/36382) key HiCache prefetch by request namespace
- [#36637](https://github.com/sgl-project/sglang/pull/36637) add free_full for tombstoned SWA nodes
</details>

<details>
<summary>Hardware & arch (8)</summary>

- [#36588](https://github.com/sgl-project/sglang/pull/36588) Intel dev branch rebase with DSv4 XPU opts
- [#36233](https://github.com/sgl-project/sglang/pull/36233) CUDA 13.4 container for initial Rubin support
- [#36434](https://github.com/sgl-project/sglang/pull/36434) ROCm 10 release images for gfx942/gfx950
- [#36892](https://github.com/sgl-project/sglang/pull/36892) rocm10 image for gfx1250
- [#34492](https://github.com/sgl-project/sglang/pull/34492) remove SGLANG_USE_SGL_XPU flag
- [#35021](https://github.com/sgl-project/sglang/pull/35021) NPU causal conv1d for Ascend KDA
- [#36849](https://github.com/sgl-project/sglang/pull/36849) NPU cp multi bs
- [#35739](https://github.com/sgl-project/sglang/pull/35739) fix NVFP4 diffusion on sm_120
</details>

<details>
<summary>API & serving (7)</summary>

- [#36626](https://github.com/sgl-project/sglang/pull/36626) resolve tool argument types through anyOf/oneOf/allOf
- [#37029](https://github.com/sgl-project/sglang/pull/37029) bound stop strings and regex patterns
- [#36754](https://github.com/sgl-project/sglang/pull/36754) diffusion rollout API: off-loop serialization, msgpack, timing headers
- [#36994](https://github.com/sgl-project/sglang/pull/36994) rollout API: return only SDE latents
- [#35127](https://github.com/sgl-project/sglang/pull/35127) extract Anthropic conversion into standalone utils
- [#36760](https://github.com/sgl-project/sglang/pull/36760) sglang-miles cherry-pick
- [#36983](https://github.com/sgl-project/sglang/pull/36983) recover multimodal decode and processor failures
</details>

<details>
<summary>Refactors (20)</summary>

- [#36789](https://github.com/sgl-project/sglang/pull/36789), [#36253](https://github.com/sgl-project/sglang/pull/36253), [#36972](https://github.com/sgl-project/sglang/pull/36972), [#36250](https://github.com/sgl-project/sglang/pull/36250), [#36621](https://github.com/sgl-project/sglang/pull/36621), [#36255](https://github.com/sgl-project/sglang/pull/36255), [#36792](https://github.com/sgl-project/sglang/pull/36792), [#36254](https://github.com/sgl-project/sglang/pull/36254) config refactor series (resolution pipeline, parallel config tiers, runtime readers)
- [#37087](https://github.com/sgl-project/sglang/pull/37087), [#37086](https://github.com/sgl-project/sglang/pull/37086) Config rounds 5.1/5.2
- [#37094](https://github.com/sgl-project/sglang/pull/37094), [#36982](https://github.com/sgl-project/sglang/pull/36982), [#37078](https://github.com/sgl-project/sglang/pull/37078), [#36958](https://github.com/sgl-project/sglang/pull/36958) move request KV fields into ReqKvInfo
- [#36586](https://github.com/sgl-project/sglang/pull/36586) refactor server argument choices
- [#36676](https://github.com/sgl-project/sglang/pull/36676) server_args constants and layout
- [#36704](https://github.com/sgl-project/sglang/pull/36704) JIT kernel and expert-pack directory layout
- [#36416](https://github.com/sgl-project/sglang/pull/36416) rename Spark3 to Spark2.5
- plus ~25 more minor config cleanups ([#36896](https://github.com/sgl-project/sglang/pull/36896), [#36620](https://github.com/sgl-project/sglang/pull/36620), [#36790](https://github.com/sgl-project/sglang/pull/36790), [#36618](https://github.com/sgl-project/sglang/pull/36618), [#36725](https://github.com/sgl-project/sglang/pull/36725), [#36975](https://github.com/sgl-project/sglang/pull/36975), [#36252](https://github.com/sgl-project/sglang/pull/36252), [#36622](https://github.com/sgl-project/sglang/pull/36622), [#36251](https://github.com/sgl-project/sglang/pull/36251), [#36973](https://github.com/sgl-project/sglang/pull/36973), [#36974](https://github.com/sgl-project/sglang/pull/36974))
</details>

<details>
<summary>Bugfixes (19)</summary>

- [#34484](https://github.com/sgl-project/sglang/pull/34484) ROCm QuickReduce fp16 saturation corrupting bf16 all-reduce
- [#34690](https://github.com/sgl-project/sglang/pull/34690) keep Qwen3-VL MoE deepstack order
- [#37043](https://github.com/sgl-project/sglang/pull/37043) preserve per-request ViT graph metadata for Qwen-VL
- [#36595](https://github.com/sgl-project/sglang/pull/36595) re-encode multimodal embeddings after cache mismatch
- [#36295](https://github.com/sgl-project/sglang/pull/36295) bound CUDA memory for fast image preprocessing
- [#35646](https://github.com/sgl-project/sglang/pull/35646) detect cross-node multimodal transport by nnodes
- [#36398](https://github.com/sgl-project/sglang/pull/36398) MiniMax-H3 dp_size>1 deadlock
- [#34053](https://github.com/sgl-project/sglang/pull/34053) account resident weight memory in KV sizing
- [#37026](https://github.com/sgl-project/sglang/pull/37026) isolate HiCache decode offload state per request
- [#36638](https://github.com/sgl-project/sglang/pull/36638) fix KeyError on batch requests freed before read
- [#34639](https://github.com/sgl-project/sglang/pull/34639) allow model_loader_extra_config with remote_instance
- [#29133](https://github.com/sgl-project/sglang/pull/29133) fix MORI-IO ABORT bootstrap handling
- [#29100](https://github.com/sgl-project/sglang/pull/29100) NPU torch>=2.8 CUDA memory-pool APIs
- [#36542](https://github.com/sgl-project/sglang/pull/36542) fix LingBot-Video text encoding
- [#36529](https://github.com/sgl-project/sglang/pull/36529) defer sgl_kernel.quantization import in expert_pack
- [#36296](https://github.com/sgl-project/sglang/pull/36296) AMD shared-KV verify tests for GQA
- [#36413](https://github.com/sgl-project/sglang/pull/36413) CPU CI failures
- [#36360](https://github.com/sgl-project/sglang/pull/36360) Intel XPU rerank hang
- [#34842](https://github.com/sgl-project/sglang/pull/34842) revert symm-mem disable for Kimi hybrid models
</details>

<details>
<summary>Diffusion (19)</summary>

- [#37075](https://github.com/sgl-project/sglang/pull/37075) fuse Wan2.2 NVFP4 bias+GELU on Blackwell
- [#36592](https://github.com/sgl-project/sglang/pull/36592) fuse Wan FFN GELU epilogue
- [#36571](https://github.com/sgl-project/sglang/pull/36571) fuse Cosmos3 Nano T2I attention on Hopper
- [#36504](https://github.com/sgl-project/sglang/pull/36504) transposed residual-gate add
- [#37090](https://github.com/sgl-project/sglang/pull/37090) cache Qwen-Image modulation across serial CFG branches
- [#35613](https://github.com/sgl-project/sglang/pull/35613) scope model-specific API parameters
- [#36883](https://github.com/sgl-project/sglang/pull/36883) resolve indexed component weight sets
- [#37004](https://github.com/sgl-project/sglang/pull/37004) stream VAE weights directly to GPU
- [#36902](https://github.com/sgl-project/sglang/pull/36902) delegate quantized components to Transformers
- [#35858](https://github.com/sgl-project/sglang/pull/35858) allow Cache-DiT with layerwise offload
- [#36327](https://github.com/sgl-project/sglang/pull/36327) bound Ulysses A2A staging buffers
- [#36832](https://github.com/sgl-project/sglang/pull/36832) avoid direct GPU parameter copies
- [#36641](https://github.com/sgl-project/sglang/pull/36641) keep Cosmos3 Nano resident on 96 GB GPUs
- [#36485](https://github.com/sgl-project/sglang/pull/36485) align video BCG warmup frame count
- [#36917](https://github.com/sgl-project/sglang/pull/36917) reject incompatible transformer fallback
- [#37049](https://github.com/sgl-project/sglang/pull/37049) component execution options fail closed
- [#36863](https://github.com/sgl-project/sglang/pull/36863) fix image encoder parallel folding
- [#36249](https://github.com/sgl-project/sglang/pull/36249) out-of-tree torch.compile backends
- [#36726](https://github.com/sgl-project/sglang/pull/36726) fix five failing unit tests
</details>

<details>
<summary>Tests, CI & build (12)</summary>

- [#36979](https://github.com/sgl-project/sglang/pull/36979) move gpqa/aime25 to sgl-eval
- [#35791](https://github.com/sgl-project/sglang/pull/35791) test-only TreeCore inspector
- [#36887](https://github.com/sgl-project/sglang/pull/36887) slim JIT kernel unit tests
- [#36281](https://github.com/sgl-project/sglang/pull/36281) GLM-5.2 per-commit unified cache CI
- [#36605](https://github.com/sgl-project/sglang/pull/36605) graceful teardown for radix_cache fixtures
- [#36205](https://github.com/sgl-project/sglang/pull/36205) gate idle-loop tree-cache check behind env
- [#34668](https://github.com/sgl-project/sglang/pull/34668) stabilize nightly precision regression
- [#36100](https://github.com/sgl-project/sglang/pull/36100) trigger pr-test-xpu on multimodal_gen changes
- [#36736](https://github.com/sgl-project/sglang/pull/36736), [#36393](https://github.com/sgl-project/sglang/pull/36393), [#36636](https://github.com/sgl-project/sglang/pull/36636) AMD CI job consolidation and labels
- [#36929](https://github.com/sgl-project/sglang/pull/36929) CUDA 13.4 image with flashinfer 0.6.18rc10
- [#37148](https://github.com/sgl-project/sglang/pull/37148) fix stale GPU capability test patches
</details>

<details>
<summary>Docs (12)</summary>

- [#36476](https://github.com/sgl-project/sglang/pull/36476) NPU best practice update
- [#36028](https://github.com/sgl-project/sglang/pull/36028) MiniMax H3 checkpoint format table
- [#36544](https://github.com/sgl-project/sglang/pull/36544), [#36519](https://github.com/sgl-project/sglang/pull/36519), [#36513](https://github.com/sgl-project/sglang/pull/36513), [#36660](https://github.com/sgl-project/sglang/pull/36660), [#36740](https://github.com/sgl-project/sglang/pull/36740), [#36608](https://github.com/sgl-project/sglang/pull/36608) GLM-5.3-Flash cookbook updates
- [#36808](https://github.com/sgl-project/sglang/pull/36808) Hy4-Preview follow-ups
- [#36977](https://github.com/sgl-project/sglang/pull/36977) cookbook accuracy via sgl-eval
- [#36364](https://github.com/sgl-project/sglang/pull/36364) Ling-3.0-flash GB10 cells
- [#37050](https://github.com/sgl-project/sglang/pull/37050) HiCache L2 private, L3 shared
- [#37092](https://github.com/sgl-project/sglang/pull/37092) AMD v4 cookbook
- plus ~6 more minor docs updates
</details>

<details>
<summary>Other (10)</summary>

- [#37098](https://github.com/sgl-project/sglang/pull/37098), [#37091](https://github.com/sgl-project/sglang/pull/37091) Unified Cache Linker external-linker support
- [#36198](https://github.com/sgl-project/sglang/pull/36198) weight cache EPLB support
- [#36299](https://github.com/sgl-project/sglang/pull/36299) weight cache daemon paths via env
- [#36739](https://github.com/sgl-project/sglang/pull/36739) fold allocator free-group flag
- [#35379](https://github.com/sgl-project/sglang/pull/35379) generalize hybrid SWA MTP draft pool routing
- [#36714](https://github.com/sgl-project/sglang/pull/36714) AMD PD DSA fused-TopK seed remap
- [#36768](https://github.com/sgl-project/sglang/pull/36768) vendor-neutral NPU quantization comments
- [#36667](https://github.com/sgl-project/sglang/pull/36667) pre-commit clean branch
- [#36778](https://github.com/sgl-project/sglang/pull/36778) /rerun-test backend reporting
- plus ~95 more merged PRs not itemized in the source data
</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (sglang.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 18485d8933f533e9387d001e59eee5087c303cb6b200909d9e98fd516a386356 -->
