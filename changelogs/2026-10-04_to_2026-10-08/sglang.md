# sglang: PR digest (2026-10-04 to 2026-10-08)

_280 merged, 428 newly opened - source sgl-project/sglang, generated 2026-10-08T16:44:09Z_

## TL;DR
- **DeepSeek-V4/V4.1 got the most attention.** Merged work covers mHC state-machine unification (`[#42245](https://github.com/sgl-project/sglang/pull/42245)`), TRT-LLM sparse attention (`[#41603](https://github.com/sgl-project/sglang/pull/41603)`), a prefill-indexer rewrite with no host syncs (`[#41659](https://github.com/sgl-project/sglang/pull/41659)`) and bounded SWA replay (`[#42273](https://github.com/sgl-project/sglang/pull/42273)`). Open PRs add SM120 decode wins, FP4 indexer work on AMD, Engram loading speedups and PDMux layerwise prefill.
- **Perf work is mostly kernel-level and Blackwell/ROCm-focused.** Merged: a sparse-MLA prefill backend for DSA on SM120/SM90 (`[#32779](https://github.com/sgl-project/sglang/pull/32779)`), a fused FP8 KV quant commit kernel (`[#40785](https://github.com/sgl-project/sglang/pull/40785)`) and DeepEP v2 expanded prefill dispatch (`[#37261](https://github.com/sgl-project/sglang/pull/37261)`). Also merged: FlashInfer A2A for MoE prefill (`[#39818](https://github.com/sgl-project/sglang/pull/39818)`) and GLM-5.2 ROCm decode tiles (`[#41725](https://github.com/sgl-project/sglang/pull/41725)`). MiniMax-M3 and GLM got decode and MTP/DFlash tuning.
- **Memory and cache architecture is shifting.** Merged: the unified-memory pool (fused draft KV for EAGLE, DFLASH and DSPARK) plus several unified HiCache fixes. Opened: trtllm_mha on the unified pool (`[#42930](https://github.com/sgl-project/sglang/pull/42930)`), paged experts (`[#42557](https://github.com/sgl-project/sglang/pull/42557)`) and OCP MXFP4 KV cache (`[#42759](https://github.com/sgl-project/sglang/pull/42759)`).
- **Direction:** a large refactor wave toward stage boundaries and per-layer parallel-group selection. Diffusion code is being deduplicated heavily, the Rust router/frontend is moving into serving /generate, chat and completions, and a 21-part LoRA MoE/dense stack is being opened.

## Most important PRs
**`[#42753](https://github.com/sgl-project/sglang/pull/42753)` Translate each KV loc once per iteration**
A 97-file refactor that moves KV location translation to once per iteration across flashinfer, triton and MLA backends. It underpins the unified-memory pool work and removes repeated translation in hot paths.

**`[#37628](https://github.com/sgl-project/sglang/pull/37628)` Fuse the draft model's KV into the target's page envelope**
This is the core mechanism for unified-memory speculative decoding: draft and target share one page envelope. Follow-ups `[#40491](https://github.com/sgl-project/sglang/pull/40491)` and `[#40492](https://github.com/sgl-project/sglang/pull/40492)` admit EAGLE/EAGLE3, DFLASH and DSPARK onto it.

**`[#32779](https://github.com/sgl-project/sglang/pull/32779)` CUDA fused Triton sparse-MLA prefill backend for DSA (SM120/SM90)**
Adds a fused sparse-MLA prefill path for DeepSeek sparse attention on consumer and Hopper parts. It reduces dependence on vendor-specific kernels.

**`[#37662](https://github.com/sgl-project/sglang/pull/37662)` FastH3 8-step V2, native Blackwell VSA, batched H3 VAE decode**
Big diffusion perf feature for MiniMax-H3 video generation, covering sparse attention on Blackwell and batched VAE decode.

**`[#42245](https://github.com/sgl-project/sglang/pull/42245)` Unify mHC into one state machine (DeepSeek-V4.1)**
Replaces medium-batch fusion variants with a single mHC state machine, removing about 1.5k lines. It simplifies the path that the many open V4.1 perf PRs build on.

## More changes by area

<details>
<summary>Performance (8)</summary>

- [#42239](https://github.com/sgl-project/sglang/pull/42239) DiffusionGemma accelerated with FA4 and CUDA graphs on Blackwell
- [#43013](https://github.com/sgl-project/sglang/pull/43013) fuse short-convolution checkpoint tracking metadata
- [#42489](https://github.com/sgl-project/sglang/pull/42489) GLM-5.3-Flash DFlash decoding improvements on B300
- [#42101](https://github.com/sgl-project/sglang/pull/42101) MiMo local audio attention optimized on Hopper
- [#41906](https://github.com/sgl-project/sglang/pull/41906) MiniMax-H3 video VAE decoder RMSNorm and QK RoPE fused
- [#41819](https://github.com/sgl-project/sglang/pull/41819) encode MP4 while the VAE decodes (MiniMax-H3, Wan)
- [#42171](https://github.com/sgl-project/sglang/pull/42171) FLUX 3 Action CUDA graphs for observation encoding and denoising
- [#41830](https://github.com/sgl-project/sglang/pull/41830) Wan VAE decoder first-decode work moved off the request path

</details>

<details>
<summary>Kernels & attention (10)</summary>

- [#41659](https://github.com/sgl-project/sglang/pull/41659) DSv4.1 prefill indexer: raw selection, no host syncs
- [#42273](https://github.com/sgl-project/sglang/pull/42273) DSv4.1 bounded replay with sparse MLA path
- [#41603](https://github.com/sgl-project/sglang/pull/41603) DSV4.1 opt-in TRT-LLM sparse attention
- [#38615](https://github.com/sgl-project/sglang/pull/38615) MiniMax-M3 decode top-k in register buckets
- [#38841](https://github.com/sgl-project/sglang/pull/38841) MiniMax-M3 decode paged K/V tile loads and tiny router GEMM
- [#42178](https://github.com/sgl-project/sglang/pull/42178) DSA k-pool uses 256-token logical page
- [#42486](https://github.com/sgl-project/sglang/pull/42486) explicit reciprocal scaling for recurrent Q/K normalization
- [#41656](https://github.com/sgl-project/sglang/pull/41656) fix XQA draft extend with FP8 KV in trtllm_mha
- [#42671](https://github.com/sgl-project/sglang/pull/42671) clarify DSA pooled-page naming and ownership
- [#42506](https://github.com/sgl-project/sglang/pull/42506) simplify GDN, vision RoPE and MLA kernel dispatch

</details>

<details>
<summary>MoE & quantization (9)</summary>

- [#37261](https://github.com/sgl-project/sglang/pull/37261) DeepEP v2 expanded prefill dispatch
- [#39818](https://github.com/sgl-project/sglang/pull/39818) FlashInfer A2A for MoE prefill instead of AG+RS
- [#42022](https://github.com/sgl-project/sglang/pull/42022) draft model picks its own W4A4 MXFP4 MegaMoE MMA type
- [#40785](https://github.com/sgl-project/sglang/pull/40785) FP8 KV quantization fused into the prefix-valid commit kernel
- [#42585](https://github.com/sgl-project/sglang/pull/42585) quantize reloaded FP8 weights after native sharding
- [#42479](https://github.com/sgl-project/sglang/pull/42479) fused MoE finalize all-reduce offered only to blocks that owe the sum
- [#40671](https://github.com/sgl-project/sglang/pull/40671) failed deep_ep import check no longer kills servers that don't use DeepEP
- [#34540](https://github.com/sgl-project/sglang/pull/34540) Quark W4A4 MXFP4 MoE clamped-SwiGLU fix on AITER
- [#41671](https://github.com/sgl-project/sglang/pull/41671) Flux3 rowwise FP8 quantization with Triton

</details>

<details>
<summary>Model support (8)</summary>

- [#42743](https://github.com/sgl-project/sglang/pull/42743) Kandinsky 6 (diffusion)
- [#42645](https://github.com/sgl-project/sglang/pull/42645) serve pplx-decider-v1.1
- [#30487](https://github.com/sgl-project/sglang/pull/30487) Ideogram TurboTime LoRA inference
- [#42174](https://github.com/sgl-project/sglang/pull/42174) Qwen-Image 2.1 fused gate_up LoRAs
- [#42556](https://github.com/sgl-project/sglang/pull/42556) community ComfyUI-GGUF Qwen-Image-2.1 transformers
- [#35857](https://github.com/sgl-project/sglang/pull/35857) MiniMax-H3 community LoRA recipes and Kohya mapping
- [#42609](https://github.com/sgl-project/sglang/pull/42609) fuse Anima FP32 split-half Q/K RoPE
- [#42480](https://github.com/sgl-project/sglang/pull/42480) GigaChat 3.5 stage boundaries built once

</details>

<details>
<summary>Parallelism & scheduling (12)</summary>

- [#42038](https://github.com/sgl-project/sglang/pull/42038) DP x TP x CP attention with interleave CP
- [#42041](https://github.com/sgl-project/sglang/pull/42041) scattered interleave CP inputs with expert parallelism
- [#42755](https://github.com/sgl-project/sglang/pull/42755) per-rank DP attention imbalance metrics
- [#42625](https://github.com/sgl-project/sglang/pull/42625) gather prefill-delayer queue timeout across ranks
- [#42822](https://github.com/sgl-project/sglang/pull/42822) replace `extend_range` with `extend_end`
- [#42824](https://github.com/sgl-project/sglang/pull/42824) track prefill progress as `prefix_len`
- [#42825](https://github.com/sgl-project/sglang/pull/42825) derive prefix KV indices from `last_node`
- [#42823](https://github.com/sgl-project/sglang/pull/42823) fold match write-back into `match_kv_cache`
- [#42537](https://github.com/sgl-project/sglang/pull/42537) streaming session owns its KV record and tree lock
- [#42539](https://github.com/sgl-project/sglang/pull/42539) count streaming session KV by owner
- [#42330](https://github.com/sgl-project/sglang/pull/42330) aborted streaming turns released via the normal path
- [#42051](https://github.com/sgl-project/sglang/pull/42051) validate PD decode state layout once at registration

</details>

<details>
<summary>Hardware & arch (12)</summary>

- [#34537](https://github.com/sgl-project/sglang/pull/34537) AMD aiter asm for kimi k3 target verify (DCP 3/N)
- [#34438](https://github.com/sgl-project/sglang/pull/34438) AMD aiter asm ps for kimi k3 prefill (DCP 2/N)
- [#41134](https://github.com/sgl-project/sglang/pull/41134) AMD small-M W8A8 FP8 GEMM for Qwen3.5 on gfx950
- [#41133](https://github.com/sgl-project/sglang/pull/41133) AMD one-launch small-M MoE router on gfx950
- [#39931](https://github.com/sgl-project/sglang/pull/39931) ROCm topk v2 splits one long row across blocks
- [#41707](https://github.com/sgl-project/sglang/pull/41707) AITER ASM prefill for MiniMax-M3 HD128 on AMD
- [#35357](https://github.com/sgl-project/sglang/pull/35357) MiniMax-M3 fused sparse QK norm/RoPE/cache writes with AITER
- [#39923](https://github.com/sgl-project/sglang/pull/39923) AMD DSV4 PCP with fp8 unified_kv on gfx950
- [#36780](https://github.com/sgl-project/sglang/pull/36780) Apple Silicon MPS platform for the Torch model runner
- [#35594](https://github.com/sgl-project/sglang/pull/35594) vendor KV pool classes and PlatformCapabilities
- [#40190](https://github.com/sgl-project/sglang/pull/40190) XPU fused QK-norm + RoPE for Qwen3-MoE
- [#42635](https://github.com/sgl-project/sglang/pull/42635) AITER unified verify without host seq_lens

</details>

<details>
<summary>API & serving, router (12)</summary>

- [#42662](https://github.com/sgl-project/sglang/pull/42662) split sglang-processor into tokenizer, render and parser
- [#42664](https://github.com/sgl-project/sglang/pull/42664) DeepSeek-V4 parity with SGLang plus a parity harness
- [#42665](https://github.com/sgl-project/sglang/pull/42665) router renders DeepSeek-V4 through sglang-processor
- [#42429](https://github.com/sgl-project/sglang/pull/42429) router reorg bucket config with per-group admission
- [#42428](https://github.com/sgl-project/sglang/pull/42428) router pressure and prefix signals moved out of legacy policies
- [#42545](https://github.com/sgl-project/sglang/pull/42545) improved balanced policy mode
- [#42628](https://github.com/sgl-project/sglang/pull/42628) retry 1/5: selection skips already-failed workers
- [#42629](https://github.com/sgl-project/sglang/pull/42629) retry 2/5: request dispatchable more than once
- [#42630](https://github.com/sgl-project/sglang/pull/42630) retry 3/5: retry failed dispatches on another worker
- [#42631](https://github.com/sgl-project/sglang/pull/42631) retry 4/5: back off between retries
- [#42632](https://github.com/sgl-project/sglang/pull/42632) retry 5/5: bound streaming time-to-headers
- [#42623](https://github.com/sgl-project/sglang/pull/42623) preserve empty K2 Horizon reasoning in chat responses

</details>

<details>
<summary>Memory & cache (HiCache) (9)</summary>

- [#39479](https://github.com/sgl-project/sglang/pull/39479) fix unified HiCache physical transfers
- [#42633](https://github.com/sgl-project/sglang/pull/42633) manage buffer-mode backups per storage pool
- [#42399](https://github.com/sgl-project/sglang/pull/42399) SeaweedFS L3 storage backend
- [#38480](https://github.com/sgl-project/sglang/pull/38480) fix host lock ownership across radix splits
- [#39862](https://github.com/sgl-project/sglang/pull/39862) carry Mamba slot side states through host tier
- [#33883](https://github.com/sgl-project/sglang/pull/33883) route `--file-storage-path` to the file backend
- [#41453](https://github.com/sgl-project/sglang/pull/41453) retire in-flight storage prefetches through one helper
- [#42923](https://github.com/sgl-project/sglang/pull/42923) `match_prefix` returns only the matched length
- [#43023](https://github.com/sgl-project/sglang/pull/43023) `init_load_back` returns only the loaded length

</details>

<details>
<summary>Bugfixes (14)</summary>

- [#39982](https://github.com/sgl-project/sglang/pull/39982) unified-memory compaction gates and pending page reuse
- [#38229](https://github.com/sgl-project/sglang/pull/38229) inkling unified-memory checkpoint destinations
- [#42072](https://github.com/sgl-project/sglang/pull/42072) unified-memory lazy checkpoint policy
- [#41927](https://github.com/sgl-project/sglang/pull/41927) mamba + PD + decode radix cache allocation crash
- [#36854](https://github.com/sgl-project/sglang/pull/36854) pin multimodal-gen ZMQ ingress to loopback
- [#41917](https://github.com/sgl-project/sglang/pull/41917) hybrid SP+TP for I2V models
- [#42494](https://github.com/sgl-project/sglang/pull/42494) AMD RoPE cache dtype and diffusion CI failures
- [#40765](https://github.com/sgl-project/sglang/pull/40765) wait for multimodal process teardown
- [#43100](https://github.com/sgl-project/sglang/pull/43100) DSA index host buffer cleanup
- [#43101](https://github.com/sgl-project/sglang/pull/43101) K-only host buffer cleanup
- [#42121](https://github.com/sgl-project/sglang/pull/42121) H3 INT8 loading in ComfyUI integrated mode
- [#38028](https://github.com/sgl-project/sglang/pull/38028) comfy-kitchen MXFP8 scales no longer interleaved twice
- [#40158](https://github.com/sgl-project/sglang/pull/40158) MiniMax-H3 QKV layout inference
- plus 3 more minor fixes folded in ([#22813](https://github.com/sgl-project/sglang/pull/22813), [#42436](https://github.com/sgl-project/sglang/pull/42436), [#42471](https://github.com/sgl-project/sglang/pull/42471))

</details>

<details>
<summary>Refactors (14)</summary>

- [#42481](https://github.com/sgl-project/sglang/pull/42481) build layer stacks in order with append_stages
- [#42587](https://github.com/sgl-project/sglang/pull/42587) parallel groups for remaining model projections
- [#42588](https://github.com/sgl-project/sglang/pull/42588) retain process groups in parallel linear layers
- [#42590](https://github.com/sgl-project/sglang/pull/42590) destination layouts for checkpoint mappings
- [#42589](https://github.com/sgl-project/sglang/pull/42589) owner partitions for auxiliary/expert checkpoint loading
- [#42586](https://github.com/sgl-project/sglang/pull/42586) vision encoders select their parallel group
- [#42426](https://github.com/sgl-project/sglang/pull/42426) linear layers select their parallel group
- [#42468](https://github.com/sgl-project/sglang/pull/42468) model MLPs select their parallel group
- [#42484](https://github.com/sgl-project/sglang/pull/42484) MLA projections select their parallel group
- [#42478](https://github.com/sgl-project/sglang/pull/42478) Qwen4 experimental decoders from stage boundaries
- [#42477](https://github.com/sgl-project/sglang/pull/42477) Hunyuan V4 decoder from stage boundaries
- [#42286](https://github.com/sgl-project/sglang/pull/42286) TCPCG: bind live batches in BCG eager calls (2/9)
- [#42285](https://github.com/sgl-project/sglang/pull/42285) TCPCG: relocate shared graph helpers (1/9)
- [#42686](https://github.com/sgl-project/sglang/pull/42686) hold a request's tree lock as one `TreeLock`

</details>

<details>
<summary>Diffusion cleanup & runtime (18)</summary>

- [#42768](https://github.com/sgl-project/sglang/pull/42768) simplify Kandinsky 6 models, SR sampling and tests
- [#42391](https://github.com/sgl-project/sglang/pull/42391) kernel validation moved into launchers
- [#42370](https://github.com/sgl-project/sglang/pull/42370) quality tiers named after what they guarantee
- [#37549](https://github.com/sgl-project/sglang/pull/37549) `--async-output-save` overlaps saving with the next request
- [#41721](https://github.com/sgl-project/sglang/pull/41721) stream an oversized DiT in auto mode instead of OOM
- [#40761](https://github.com/sgl-project/sglang/pull/40761) skip warmup preload when it would OOM
- [#41718](https://github.com/sgl-project/sglang/pull/41718) release allocator cache when idle
- [#41710](https://github.com/sgl-project/sglang/pull/41710) stop specializing kernels on per-request sequence lengths
- [#42843](https://github.com/sgl-project/sglang/pull/42843) dedupe Qwen Image RoPE and SenseNova backbones
- [#42841](https://github.com/sgl-project/sglang/pull/42841) share KL VAE encode/decode and tiling
- [#42848](https://github.com/sgl-project/sglang/pull/42848) share sigma schedules and causal cross-attention
- [#42856](https://github.com/sgl-project/sglang/pull/42856) share ModelOpt checkpoint conversion I/O
- [#42866](https://github.com/sgl-project/sglang/pull/42866) dedupe VAE resampling and LTX tiling
- [#42988](https://github.com/sgl-project/sglang/pull/42988) share stacked encoder weight loading
- [#42908](https://github.com/sgl-project/sglang/pull/42908) dedupe KL VAE attention processor management
- [#43002](https://github.com/sgl-project/sglang/pull/43002) dedupe FLUX positions and RoPE
- plus 2 more small diffusion dedups ([#42983](https://github.com/sgl-project/sglang/pull/42983), [#42967](https://github.com/sgl-project/sglang/pull/42967))

</details>

<details>
<summary>Tests (6)</summary>

- [#43081](https://github.com/sgl-project/sglang/pull/43081) remove unregistered chunked-prefill tests under test/manual
- [#42571](https://github.com/sgl-project/sglang/pull/42571) drop redundant tc_piecewise tests
- [#42518](https://github.com/sgl-project/sglang/pull/42518) require every ComponentData field to be classified by split hooks
- [#39839](https://github.com/sgl-project/sglang/pull/39839) cover SWA admission after declined HiCache restores
- [#40404](https://github.com/sgl-project/sglang/pull/40404) NPU cudagraph runner unit tests
- [#42860](https://github.com/sgl-project/sglang/pull/42860) dedupe Qwen-VL inputs and accuracy suites

</details>

<details>
<summary>CI & build (10)</summary>

- [#38641](https://github.com/sgl-project/sglang/pull/38641) upgrade CUDA PyTorch stack to 2.14
- [#42784](https://github.com/sgl-project/sglang/pull/42784) bump transformers to 5.19.0
- [#42612](https://github.com/sgl-project/sglang/pull/42612) uv-managed Python 3.12 in the CUDA image
- [#42827](https://github.com/sgl-project/sglang/pull/42827) one DeepEP ref for implementation and packaging
- [#42661](https://github.com/sgl-project/sglang/pull/42661) fix nightly-cu134 build
- [#42602](https://github.com/sgl-project/sglang/pull/42602) AMD M3-MXFP4 nightly test
- [#41476](https://github.com/sgl-project/sglang/pull/41476) DeepSeek-V4.1-Flash MI35x nightly accuracy test
- [#42771](https://github.com/sgl-project/sglang/pull/42771) nightly-test miles ROCm image on MI300
- [#38520](https://github.com/sgl-project/sglang/pull/38520) docs drift check for server_arguments.mdx
- plus 2 more diffusion CI baseline/timing updates ([#42986](https://github.com/sgl-project/sglang/pull/42986), [#42329](https://github.com/sgl-project/sglang/pull/42329))

</details>

<details>
<summary>Docs (6)</summary>

- [#41585](https://github.com/sgl-project/sglang/pull/41585) sglang API specs
- [#42726](https://github.com/sgl-project/sglang/pull/42726) InferenceX AgentX cookbook for GLM-5.2 and DeepSeek-V4/V4.1
- [#42757](https://github.com/sgl-project/sglang/pull/42757) MI355X DeepSeek-V4 Pro PD recipes
- [#42847](https://github.com/sgl-project/sglang/pull/42847) AMD V4.1 cookbook update
- [#42167](https://github.com/sgl-project/sglang/pull/42167) GLM-5.2 GB300 AgentX recipe moved to HiCache section
- [#42512](https://github.com/sgl-project/sglang/pull/42512) AMD mori io and umbp playground fix

</details>

<details>
<summary>Newly opened (in progress) highlights (16)</summary>

- [#42555](https://github.com/sgl-project/sglang/pull/42555), [#42532](https://github.com/sgl-project/sglang/pull/42532), [#42707](https://github.com/sgl-project/sglang/pull/42707), [#42531](https://github.com/sgl-project/sglang/pull/42531), [#42698](https://github.com/sgl-project/sglang/pull/42698) cake_kernels routes (DSA indexer via FlashInfer, SP all-gather matmul, MiniMax-H3, Kimi-K3 FP8 projection)
- [#42839](https://github.com/sgl-project/sglang/pull/42839) Kimi-K3 Gluon whole-layer KDA and attention kernels on AMD
- [#42930](https://github.com/sgl-project/sglang/pull/42930) trtllm_mha on the unified pool with decode graphs and spec decoding
- [#42868](https://github.com/sgl-project/sglang/pull/42868) through [#42888](https://github.com/sgl-project/sglang/pull/42888) a 21-part LoRA stack: dense and MoE kernels, plans, CuTeDSL and Marlin providers
- [#42514](https://github.com/sgl-project/sglang/pull/42514), [#42513](https://github.com/sgl-project/sglang/pull/42513), [#42509](https://github.com/sgl-project/sglang/pull/42509), [#42507](https://github.com/sgl-project/sglang/pull/42507) PDMux for DeepSeek-V4.1-Flash: layerwise MTP/DSpark, prefill and decode DP alignment, HiCache
- [#42864](https://github.com/sgl-project/sglang/pull/42864), [#43008](https://github.com/sgl-project/sglang/pull/43008), [#42921](https://github.com/sgl-project/sglang/pull/42921), [#42715](https://github.com/sgl-project/sglang/pull/42715) DSv4.1 SM120 and replay perf: split-K mHC, exact FP8 WO-A, history checks
- [#43057](https://github.com/sgl-project/sglang/pull/43057) fused sharded DSA indexer and raw FP8 KV stores
- [#42759](https://github.com/sgl-project/sglang/pull/42759) and [#43105](https://github.com/sgl-project/sglang/pull/43105) OCP MXFP4 KV via FlashMLA (SM100) and GLM DSA NVFP4 KV (SM120)
- [#42557](https://github.com/sgl-project/sglang/pull/42557) Paged Experts for MoE models that exceed VRAM
- [#42650](https://github.com/sgl-project/sglang/pull/42650) FlashInfer SSD prefill for Mamba2
- [#42802](https://github.com/sgl-project/sglang/pull/42802) and [#43052](https://github.com/sgl-project/sglang/pull/43052) spec-decode verification sampling in CUDA graphs and draft sampling overrides
- [#42998](https://github.com/sgl-project/sglang/pull/42998), [#42997](https://github.com/sgl-project/sglang/pull/42997), [#42999](https://github.com/sgl-project/sglang/pull/42999), [#43000](https://github.com/sgl-project/sglang/pull/43000) router serving /v1/chat/completions, /v1/completions and tool calls through /generate; DeepSeek-V4.1 Flash via sglang-processor
- [#42449](https://github.com/sgl-project/sglang/pull/42449) and [#42447](https://github.com/sgl-project/sglang/pull/42447) Valkey-backed kv-indexer
- [#42938](https://github.com/sgl-project/sglang/pull/42938), [#42979](https://github.com/sgl-project/sglang/pull/42979), [#43001](https://github.com/sgl-project/sglang/pull/43001), [#43036](https://github.com/sgl-project/sglang/pull/43036) MPS/MLX exported region: compiled decode, batched prefill, logits and logprobs
- [#42618](https://github.com/sgl-project/sglang/pull/42618) and [#42973](https://github.com/sgl-project/sglang/pull/42973) DCP for GLM-5/DSV3.2 on ROCm and KV sharding for GLM DSA
- [#42540](https://github.com/sgl-project/sglang/pull/42540) refresh of CI test est_time values

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (sglang.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: f87e63cc5543c978c36b8449ae68302efad3bd5af0011000857507b82cff54af -->
