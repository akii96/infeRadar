# sglang: PR digest (2026-08-19 to 2026-08-23)

_278 merged, 407 newly opened - source sgl-project/sglang, generated 2026-08-23T21:46:54Z_

## TL;DR
- **MiniMax and DeepSeek** dominated model-specific work. MiniMax saw extensive multimodal/diffusion additions (H3 support, ComfyUI integration, native encoders), while DeepSeek-V4 received major performance upgrades including Q8KV8 sparse MLA prefill and W4A4 MegaMoE support.
- **KV Cache & Memory Architecture** took a massive leap forward with a new process-local in-memory KV indexer, HiCache buffer-only mode, and unified radix tree improvements for hybrid models.
- **Speculative Decoding** expanded significantly, adding multi-adapter LoRA support for EAGLE/NEXTN/DFLASH/DSPARK, and introducing DFlash2 local convolution and candidate selection.
- **Hardware & Backend** saw a major MLX/Torch 2.13 upgrade for Apple Silicon, alongside deep AMD ROCm optimizations (Radix-4 MoE routing, MI355X bpreshuffle elimination) and Ascend NPU fixes.

## Most important PRs
- **[#33829](https://github.com/sgl-project/sglang/pull/33829)** Complete dots.note.omni support with native encoders, video preprocessing, and MTP decoding. This major feature expands multimodal capabilities and introduces native MTP decoding.
- **[#33370](https://github.com/sgl-project/sglang/pull/33370)** Add process-local in-memory KV indexer and Router integration. This significantly improves KV cache management and routing performance by keeping the indexer process-local.
- **[#35758](https://github.com/sgl-project/sglang/pull/35758)** (open) Massive Qwen 3.8 rebase touching FlashInfer, Triton, MoE, MLA, and speculative decoding. This in-progress work brings comprehensive support for the latest Qwen architecture.
- **[#32984](https://github.com/sgl-project/sglang/pull/32984)** Upgrade to Torch 2.13/MLX 0.32+ and redesign the Torch-MLX tensor bridge. This major upgrade modernizes the Apple Silicon backend and improves tensor bridging efficiency.
- **[#32327](https://github.com/sgl-project/sglang/pull/32327)** Add Q8KV8 sparse MLA prefill runtime backend for DeepSeek-V4. This delivers a substantial performance win for DeepSeek models by optimizing sparse MLA prefill.

## More changes by area

<details>
<summary>Performance (10)</summary>

- [#35318](https://github.com/sgl-project/sglang/pull/35318) Overlap page preprocessing, pack the ViT, and enable prefill CUDA graph for PaddleOCR-VL
- [#33880](https://github.com/sgl-project/sglang/pull/33880) Reduce MiniMax H3 MPS memory pressure
- [#35559](https://github.com/sgl-project/sglang/pull/35559) Fix performance bug in NPU GLM 5 PP/CP optimization
- [#32832](https://github.com/sgl-project/sglang/pull/32832) Bypass caches for peer traffic in ROCm custom all-reduce
- [#35716](https://github.com/sgl-project/sglang/pull/35716) Optimize NPU GLM 5 origin dual stream
- [#35499](https://github.com/sgl-project/sglang/pull/35499) Improve Kimi-K3 DSpark draft attention kernel performance on AMD
- [#36004](https://github.com/sgl-project/sglang/pull/36004) Use full 1024-thread block for indexer top-k on ROCm for DeepSeek-V4
- [#35735](https://github.com/sgl-project/sglang/pull/35735) (open) Split the custom all-reduce communicator into push/pull planes
- [#35710](https://github.com/sgl-project/sglang/pull/35710) (open) Cut device syncs and redundant launches from decode scheduling
- [#35760](https://github.com/sgl-project/sglang/pull/35760) (open) Tune the W4AFP8 DeepEP low-latency requant launch geometry
</details>

<details>
<summary>Kernels & attention (38)</summary>

- [#29525](https://github.com/sgl-project/sglang/pull/29525) Add DeepEPv2 (ElasticBuffer) MoE A2A backend
- [#35568](https://github.com/sgl-project/sglang/pull/35568) Revert DeepEPv2 (ElasticBuffer) MoE A2A backend
- [#35006](https://github.com/sgl-project/sglang/pull/35006) Reuse SRT Qwen vision and text modules for diffusion
- [#35370](https://github.com/sgl-project/sglang/pull/35370) Load GGUF transformer checkpoints for MiniMax-H3
- [#33249](https://github.com/sgl-project/sglang/pull/33249) Integrate MoonEP BF16 PoC for Kimi-K3
- [#35339](https://github.com/sgl-project/sglang/pull/35339) Add per-request lossy accelerations (Cache-DiT, CFG gating, attention backend override)
- [#34490](https://github.com/sgl-project/sglang/pull/34490) Add Radix-4 MoE top-k router kernel for Kimi-K3 routing on AMD
- [#35371](https://github.com/sgl-project/sglang/pull/35371) Add DFlash2 local convolution and candidate selector
- [#32577](https://github.com/sgl-project/sglang/pull/32577) Add AITer fused mHC post+pre with cross-layer boundary dispatch for DeepSeek-V4
- [#34859](https://github.com/sgl-project/sglang/pull/34859) Add Qwen3.8-27B model support
- [#35698](https://github.com/sgl-project/sglang/pull/35698) Fuse LTX-2.5 decoder 3D RoPE
- [#34680](https://github.com/sgl-project/sglang/pull/34680) Support subblock sparse attention on SM90 for MiniMax H3
- [#35796](https://github.com/sgl-project/sglang/pull/35796) Fall back to a component's default attention backend
- [#35695](https://github.com/sgl-project/sglang/pull/35695) Fuse SANA-Video interleaved RoPE
- [#35175](https://github.com/sgl-project/sglang/pull/35175) Route the ragged prefill top-k to the v2 kernel
- [#32340](https://github.com/sgl-project/sglang/pull/32340) Add shared experts fusion top6 for DeepSeek-V4 on AMD
- [#35041](https://github.com/sgl-project/sglang/pull/35041) Trim top-k v2 output modes and tighten its PDL waits
- [#33166](https://github.com/sgl-project/sglang/pull/33166) Eliminate bpreshuffle fp8-scale copies at producer sites for DeepSeek-V4 on MI355X
- [#35569](https://github.com/sgl-project/sglang/pull/35569) Add NPU support for TP
- [#33165](https://github.com/sgl-project/sglang/pull/33165) Eliminate bpreshuffle fp8-scale relayout copy in dense w8a8 linear for DeepSeek-V4 on MI355X
- [#35432](https://github.com/sgl-project/sglang/pull/35432) Support 950 GLM cache service on NPU
- [#35405](https://github.com/sgl-project/sglang/pull/35405) Fix SM107 MXFP8 activation prep
- [#35228](https://github.com/sgl-project/sglang/pull/35228) Load compressed-tensors quantized lm_head instead of value-casting it
- [#35077](https://github.com/sgl-project/sglang/pull/35077) Support Kimi-K3 ModelOpt mixed NVFP4/FP8 checkpoint
- [#35846](https://github.com/sgl-project/sglang/pull/35846) (open) Integrate FlashInfer MSA on Blackwell for MiniMax
- [#35731](https://github.com/sgl-project/sglang/pull/35731) (open) Integrate FlashInfer source MSA for MiniMax-M3
- [#36059](https://github.com/sgl-project/sglang/pull/36059) (open) Add native H16 CuTe sparse prefill backend for DeepSeek-V4
- [#35429](https://github.com/sgl-project/sglang/pull/35429) (open) Add SM80 Torch fallbacks and Triton paged-MQA indexer
- [#35444](https://github.com/sgl-project/sglang/pull/35444) (open) Add strict FlashInfer SSD and Cake prefill backends for Mamba
- [#35977](https://github.com/sgl-project/sglang/pull/35977) (open) Add MPS backend paged attention decode for Apple Silicon
- [#35899](https://github.com/sgl-project/sglang/pull/35899) (open) Add b12x compressed-MLA branch for DSv4-Flash
- [#35807](https://github.com/sgl-project/sglang/pull/35807) (open) Serve varlen absorbed MLA under both tc_piecewise and breakable prefill CUDA graphs
- [#35850](https://github.com/sgl-project/sglang/pull/35850) (open) Restrict MiniMax-H3 SubBlock sparsity to video queries
- [#35435](https://github.com/sgl-project/sglang/pull/35435) (open) Add group-aware CPU SHM collective kernels
- [#35770](https://github.com/sgl-project/sglang/pull/35770) (open) Optimize Kimi-K3 Triton MLA prefill on gfx950
- [#35670](https://github.com/sgl-project/sglang/pull/35670) (open) Support DSpark compact verify graph and folded verify epilogue on NPU
- [#35523](https://github.com/sgl-project/sglang/pull/35523) (open) Add moonmath MLA attention backend for decode and speculative verify on gfx942
- [#35684](https://github.com/sgl-project/sglang/pull/35684) (open) Add MiniMax-H3 Spectrum skip-step and fused RMSNorm/AdaLN
</details>

<details>
<summary>MoE & quantization (18)</summary>

- [#35418](https://github.com/sgl-project/sglang/pull/35418) Support MiniMax-H3 pruned safetensors checkpoints
- [#36023](https://github.com/sgl-project/sglang/pull/36023) Load serialized Comfy ConvRot INT8 native encoders
- [#35945](https://github.com/sgl-project/sglang/pull/35945) Load serialized BnB4 components with Transformers
- [#35873](https://github.com/sgl-project/sglang/pull/35873) Fail closed for unsupported quantized component checkpoints
- [#35172](https://github.com/sgl-project/sglang/pull/35172) Extract shared checkpoint quant metadata resolver
- [#35994](https://github.com/sgl-project/sglang/pull/35994) Load serialized Comfy ConvRot INT8 DiTs
- [#35979](https://github.com/sgl-project/sglang/pull/35979) Support single-file component weight overrides
- [#35459](https://github.com/sgl-project/sglang/pull/35459) (open) Add MXFP8 x BF16 MegaMOE support
- [#35634](https://github.com/sgl-project/sglang/pull/35634) (open) Add DeepEPv2 (ElasticBuffer) MoE A2A backend
- [#35934](https://github.com/sgl-project/sglang/pull/35934) (open) Add zero-copy eager expert output path for MoonEP
- [#36043](https://github.com/sgl-project/sglang/pull/36043) (open) Add Qwen3.8 NVFP4 skinny GEMM for SM120
- [#35619](https://github.com/sgl-project/sglang/pull/35619) (open) Integrate Aiter MegaMoEv2 for DeepSeek-V4
- [#35441](https://github.com/sgl-project/sglang/pull/35441) (open) Add MXFP scheme support for AR
- [#36063](https://github.com/sgl-project/sglang/pull/36063) (open) Reuse SRT quantization contracts and MXFP8 kernels
- [#36052](https://github.com/sgl-project/sglang/pull/36052) (open) Load self-describing Quanto INT8 encoders
- [#36036](https://github.com/sgl-project/sglang/pull/36036) (open) Load serialized Comfy W4A8 checkpoints
- [#36035](https://github.com/sgl-project/sglang/pull/36035) (open) Add component-scoped quantization overrides
- [#36046](https://github.com/sgl-project/sglang/pull/36046) (open) Load Comfy NVFP4-AWQ text encoders
</details>

<details>
<summary>Parallelism & scheduling (34)</summary>

- [#30398](https://github.com/sgl-project/sglang/pull/30398) Refactor EPD for distributed and scheduler components
- [#35239](https://github.com/sgl-project/sglang/pull/35239) Refactor Rust server integration
- [#34798](https://github.com/sgl-project/sglang/pull/34798) Add buffer-only mode for HiCache host memory layer
- [#35906](https://github.com/sgl-project/sglang/pull/35906) Project the config bags from the resolution result
- [#35905](https://github.com/sgl-project/sglang/pull/35905) Record resolution writes in a declaration stash
- [#35747](https://github.com/sgl-project/sglang/pull/35747) Add sampling observer auxiliary output hooks
- [#34337](https://github.com/sgl-project/sglang/pull/34337) Support multi-adapter LoRA with EAGLE/NEXTN/DFLASH/DSPARK speculative decoding
- [#35907](https://github.com/sgl-project/sglang/pull/35907) Constructing a config no longer resolves it
- [#34406](https://github.com/sgl-project/sglang/pull/34406) Add TP/PP Consensus checker
- [#35908](https://github.com/sgl-project/sglang/pull/35908) Borrowed-record reads follow the config bags
- [#35269](https://github.com/sgl-project/sglang/pull/35269) Support runtime attach/detach for historage in UnifiedTree
- [#27770](https://github.com/sgl-project/sglang/pull/27770) Add decode-side radix cache for SWA hybrid models
- [#35360](https://github.com/sgl-project/sglang/pull/35360) Defer decode-side KV release for the NIXL backend
- [#35904](https://github.com/sgl-project/sglang/pull/35904) Ensure defensive publish does not re-project over a live process
- [#35543](https://github.com/sgl-project/sglang/pull/35543) Allow a retraction host pool smaller than the device pool
- [#35496](https://github.com/sgl-project/sglang/pull/35496) Support quantized target lm_head in the DFlash2 selector
- [#36069](https://github.com/sgl-project/sglang/pull/36069) (open) Add InferCast time predictor adapter
- [#35687](https://github.com/sgl-project/sglang/pull/35687) (open) Add optional external-cache linker mode to Unified Radix Cache
- [#35488](https://github.com/sgl-project/sglang/pull/35488) (open) Use HiCache as the plugin logical KV pool
- [#35865](https://github.com/sgl-project/sglang/pull/35865) (open) Implement DeepSeek V4 DCP on ROCm
- [#35791](https://github.com/sgl-project/sglang/pull/35791) (open) Route unified cache tests through the TreeCore interface
- [#35635](https://github.com/sgl-project/sglang/pull/35635) (open) Support partial-page prefix reuse in RadixCache
- [#35800](https://github.com/sgl-project/sglang/pull/35800) (open) Split draft SWA into committed sidecar KV and verify scratch
- [#35678](https://github.com/sgl-project/sglang/pull/35678) (open) Rebase PCP implementation
- [#35926](https://github.com/sgl-project/sglang/pull/35926) (open) Report per-token weight-version spans in generation meta info
- [#35637](https://github.com/sgl-project/sglang/pull/35637) (open) Improve Agentic RL Rollout Inference Efficiency with Uniboost Scheduler Policy
- [#35835](https://github.com/sgl-project/sglang/pull/35835) (open) Add Qwen3.5 speculative decoding on CPU
- [#35577](https://github.com/sgl-project/sglang/pull/35577) (open) Add Mooncake GPU-direct SpecForge capture
- [#35494](https://github.com/sgl-project/sglang/pull/35494) (open) Isolate C4 compress state per request for DeepSeek-V4
- [#35592](https://github.com/sgl-project/sglang/pull/35592) (open) Decide SWA slot liveness on the host instead of a device-side mask
- [#35954](https://github.com/sgl-project/sglang/pull/35954) (open) Prevent one-at-a-time DFlash/DSpark replacement prefills below the request limit
- [#35629](https://github.com/sgl-project/sglang/pull/35629) (open) Adapt DFlash2 speculative decoding to Ascend NPUs
- [#35958](https://github.com/sgl-project/sglang/pull/35958) (open) Optimize decoding procedure on Qwen3.5 for NPU
- [#35624](https://github.com/sgl-project/sglang/pull/35624) (open) Bound DSpark rejection sampling workspace
</details>

<details>
<summary>API & serving (29)</summary>

- [#29656](https://github.com/sgl-project/sglang/pull/29656) Make multimodal inputs msgpack-native
- [#35679](https://github.com/sgl-project/sglang/pull/35679) Refresh eager optimization skills and benchmark safeguards
- [#35910](https://github.com/sgl-project/sglang/pull/35910) Publish before the launcher reads effective configuration
- [#35352](https://github.com/sgl-project/sglang/pull/35352) Add a MiniMax-H3 node and a generic extra-fields passthrough for ComfyUI
- [#35641](https://github.com/sgl-project/sglang/pull/35641) Plan pinned host memory against the cgroup cap not the machine
- [#35868](https://github.com/sgl-project/sglang/pull/35868) Preserve PEFT LoRA semantics
- [#33518](https://github.com/sgl-project/sglang/pull/33518) Add sglext_spec to API
- [#35668](https://github.com/sgl-project/sglang/pull/35668) Add weight source reader
- [#35701](https://github.com/sgl-project/sglang/pull/35701) Let offloaded weights stay on the checkpoint mapping
- [#36076](https://github.com/sgl-project/sglang/pull/36076) Support compact Qwen3-VL conditioning for MiniMax H3
- [#33279](https://github.com/sgl-project/sglang/pull/33279) Add Weight Daemon abstraction
- [#35598](https://github.com/sgl-project/sglang/pull/35598) Mirror support MiniMax H3 t2va rollout
- [#35463](https://github.com/sgl-project/sglang/pull/35463) Split Pixtral multi-image features before the CUDA IPC wrap
- [#35713](https://github.com/sgl-project/sglang/pull/35713) Support out-of-tree models and pipelines
- [#35618](https://github.com/sgl-project/sglang/pull/35618) Report where a component's weights are
- [#35986](https://github.com/sgl-project/sglang/pull/35986) Re-home decode-dtype VAE weights to a file-backed store
- [#36101](https://github.com/sgl-project/sglang/pull/36101) (open) Discover weight daemons by GPU UUID and config
- [#35960](https://github.com/sgl-project/sglang/pull/35960) (open) Refactor ComfyUI integrated mode onto native pipelines and adapters
- [#35658](https://github.com/sgl-project/sglang/pull/35658) (open) Add FlashBoot load format integration
- [#35613](https://github.com/sgl-project/sglang/pull/35613) (open) Scope model-specific API parameters
- [#35829](https://github.com/sgl-project/sglang/pull/35829) (open) Support LongCat-Image-Edit and LongCat-Image-Edit-Turbo
- [#35594](https://github.com/sgl-project/sglang/pull/35594) (open) Introduce SRTPlatform.build_kv_pool request seam
- [#35936](https://github.com/sgl-project/sglang/pull/35936) (open) Prevent zombie requests after client disconnect
- [#35599](https://github.com/sgl-project/sglang/pull/35599) (open) Support NemotronH_Omni_Reasoning_V3
- [#35963](https://github.com/sgl-project/sglang/pull/35963) (open) Add Spark3 Model
- [#35516](https://github.com/sgl-project/sglang/pull/35516) (open) Extract OpenAI request preparation from inference handlers
- [#35680](https://github.com/sgl-project/sglang/pull/35680) (open) Add Vast.ai dev-install script for PP activation-compression research
- [#35693](https://github.com/sgl-project/sglang/pull/35693) (open) Preserve deferred ToolSearch on generic templates
- [#35625](https://github.com/sgl-project/sglang/pull/35625) (open) Make streaming tool-call parsing agree with non-streaming
</details>

<details>
<summary>Hardware & arch (3)</summary>

- [#35815](https://github.com/sgl-project/sglang/pull/35815) Support Ascend Mamba states with FIA and async IO
- [#33313](https://github.com/sgl-project/sglang/pull/33313) Route decode wo_a bf16 batched matmul to aiter batched_gemm_bf16 for DeepSeek-V4 on AMD
- [#35780](https://github.com/sgl-project/sglang/pull/35780) (open) Use fused Triton MRoPE for Qwen3.x on NPU
</details>

<details>
<summary>Tests, CI & build (17)</summary>

- [#35511](https://github.com/sgl-project/sglang/pull/35511) Add MiniMax-H3 ref2va audio consistency coverage and guard peak VRAM
- [#35407](https://github.com/sgl-project/sglang/pull/35407) Trim the base-c 4-gpu-h100 stage from 5 shards to 4
- [#35909](https://github.com/sgl-project/sglang/pull/35909) Pin two orderings resolution relies on
- [#35610](https://github.com/sgl-project/sglang/pull/35610) Harden CI dependencies and diffusion warmup for MUSA
- [#30984](https://github.com/sgl-project/sglang/pull/30984) Upgrade Python 3.12, Torch 2.11, and Triton 3.7 in ROCm 7.2.4
- [#34855](https://github.com/sgl-project/sglang/pull/34855) Fix critical Ascend NPU Diffusion regression and restore 2-NPU CI testcase
- [#35502](https://github.com/sgl-project/sglang/pull/35502) Add three new test cases
- [#35750](https://github.com/sgl-project/sglang/pull/35750) Gate `/rerun-test` on commenter trust and remove `/rerun-stage`
- [#35603](https://github.com/sgl-project/sglang/pull/35603) Run both ROCm 7.2.4 and ROCm 7.2.0 images on nightly test AMD
- [#32570](https://github.com/sgl-project/sglang/pull/32570) Add GLM-5.2 MI35x nightly accuracy and perf benchmark
- [#35621](https://github.com/sgl-project/sglang/pull/35621) (open) Root the JIT kernel cache under SGLANG_CACHE_DIR
- [#36016](https://github.com/sgl-project/sglang/pull/36016) (open) Refresh quality and BCG benchmark skills
- [#35472](https://github.com/sgl-project/sglang/pull/35472) (open) Run selected NPU nightly suites
- [#35951](https://github.com/sgl-project/sglang/pull/35951) (open) Clean up forkserver orphan processes and restrict nightly NPU tests to accuracy
- [#35500](https://github.com/sgl-project/sglang/pull/35500) (open) Isolate multi-node tests by run_id to prevent concurrent-run conflicts
- [#36064](https://github.com/sgl-project/sglang/pull/36064) (open) Add accuracy evaluation to benchmark.serving
- [#36073](https://github.com/sgl-project/sglang/pull/36073) (open) Add PD combo scenario unit tests
</details>

<details>
<summary>Docs (9)</summary>

- [#34247](https://github.com/sgl-project/sglang/pull/34247) Standardize diffusion cookbook model pages
- [#35597](https://github.com/sgl-project/sglang/pull/35597) Add a comment style rule to .claude/rules
- [#35816](https://github.com/sgl-project/sglang/pull/35816) Add tuning guide for H3 on consumer-level GPU
- [#35508](https://github.com/sgl-project/sglang/pull/35508) Add Ascend NPU (A3) recipe to the Kimi-K3 cookbook
- [#35794](https://github.com/sgl-project/sglang/pull/35794) Add SGLang Granite SWA support via existing Granite models
- [#35622](https://github.com/sgl-project/sglang/pull/35622) Trim restating comments and docstrings in srt/managers
- [#35825](https://github.com/sgl-project/sglang/pull/35825) Re-measure the Qwen3.8-27B RTX 5090, RTX PRO 6000 and DGX Spark grids
- [#35638](https://github.com/sgl-project/sglang/pull/35638) (open) Ratchet the allocator and pool_host layout documentation
- [#36091](https://github.com/sgl-project/sglang/pull/36091) (open) Add NPU profiler analysis skill
</details>

<details>
<summary>Refactors (6)</summary>

- [#35306](https://github.com/sgl-project/sglang/pull/35306) Move DSAIndexerPoolHost to pool_host.dsa
- [#35867](https://github.com/sgl-project/sglang/pull/35867) Hand out pinned host memory per layer
- [#35183](https://github.com/sgl-project/sglang/pull/35183) Gate native encoder quantized checkpoints
- [#35976](https://github.com/sgl-project/sglang/pull/35976) (open) Drop dead NSA/Marlin shims and classify unit tests
- [#35426](https://github.com/sgl-project/sglang/pull/35426) (open) Deprecate Prefill CP V1
- [#35647](https://github.com/sgl-project/sglang/pull/35647) (open) Extract KVCache and BaseSWAKVPool into pool/base.py
</details>

<details>
<summary>Bugfixes (9)</summary>

- [#34237](https://github.com/sgl-project/sglang/pull/34237) Recover tool calls dropped by common model-output in lfm2 detector
- [#32611](https://github.com/sgl-project/sglang/pull/32611) Fix transcription and audio-understanding for ASR/audio/speech models
- [#35818](https://github.com/sgl-project/sglang/pull/35818) Harden SafeUnpickler with exact-name allowlist for generic modules
- [#35774](https://github.com/sgl-project/sglang/pull/35774) Resolve LoRA weight sources deterministically
- [#35882](https://github.com/sgl-project/sglang/pull/35882) Transfer mapped layers through a courier thread
- [#35769](https://github.com/sgl-project/sglang/pull/35769) Fix buffer-mode HiCache load-back ownership races and add optional prefetch anchor lock
- [#26510](https://github.com/sgl-project/sglang/pull/26510) Fix _GenerationStreamAccumulator logprob_end off-by-one under retract
- [#36062](https://github.com/sgl-project/sglang/pull/36062) (open) Cache LoRA-merged weights in files the page cache can hold
- [#35725](https://github.com/sgl-project/sglang/pull/35725) (open) Route DFlash/DSpark commits through ReplaySSM spec fold
</details>

<details>
<summary>Other (11)</summary>

- plus 11 more minor updates including [#35990](https://github.com/sgl-project/sglang/pull/35990), [#36039](https://github.com/sgl-project/sglang/pull/36039), [#36055](https://github.com/sgl-project/sglang/pull/36055), [#36037](https://github.com/sgl-project/sglang/pull/36037), [#35792](https://github.com/sgl-project/sglang/pull/35792), [#36068](https://github.com/sgl-project/sglang/pull/36068), [#36084](https://github.com/sgl-project/sglang/pull/36084), [#35504](https://github.com/sgl-project/sglang/pull/35504), [#36056](https://github.com/sgl-project/sglang/pull/36056), [#35981](https://github.com/sgl-project/sglang/pull/35981), [#35606](https://github.com/sgl-project/sglang/pull/35606)
</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (sglang.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 20ecbf5bb563e000ab59d35b504ba4076a10a407ab2f293b28d352fcd22dfcb7 -->
