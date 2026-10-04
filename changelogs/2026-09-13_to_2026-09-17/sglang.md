# sglang: PR digest (2026-09-13 to 2026-09-17)

_249 merged, 461 newly opened - source sgl-project/sglang, generated 2026-09-17T14:42:02Z_

## TL;DR
- **DeepSeek-V4.1 dominated the window.** Most of the merged kernel and wrapper work landed as a "dsv4.1:" stack (top-k, compression/KV I/O, RoPE/FP4 packing, mHC, Hopper FP8 matmul, NVLink collectives). Large stacked PRs are open for PD, CP, DP-attention, and MegaMoE w4a4.
- **GLM-5.x and MiniMax-M3 were the next most active models.** GLM-5.3-Flash work covers KDA/mHC fusion, DSA draft graphs, and H20 FP8 MoE configs. MiniMax-M3 work covers SM90 Q8K8 sparse prefill, DSpark, and MXFP8 SwiGLU fusion.
- **Memory and cache work is heavy.** Merged: unified hybrid-SWA shared byte budget, HiCache buffer-mode prefetch rework, and a PD KV checksum. Open: many page-unified HiCache layout and linker PRs.
- **Direction:** a DSV4.1 launch with hardware-specific kernels (Hopper, SM120, gfx950, NPU), plus continued investment in the Rust router (cache-aware, tier-aware routing, drain, and sampling contracts).

## Most important PRs
**[#39370](https://github.com/sgl-project/sglang/pull/39370) [DSV4.1] Combine DSpark decode and prefill kernel optimizations**
Merges DSpark speculative-decode and prefill kernel optimizations for DeepSeek-V4.1 across attention, MoE, and quantization (~5k lines). It is the core performance landing for V4.1 on NVIDIA.

**[#39646](https://github.com/sgl-project/sglang/pull/39646) dsv4.1: standalone kernels and Python wrappers**
Part of the V4.1 kernel stack (with [#39652](https://github.com/sgl-project/sglang/pull/39652), [#39648](https://github.com/sgl-project/sglang/pull/39648), [#39653](https://github.com/sgl-project/sglang/pull/39653), [#39656](https://github.com/sgl-project/sglang/pull/39656), [#39657](https://github.com/sgl-project/sglang/pull/39657)). Adds the standalone attention, quantization, and speculative-decode kernels the V4.1 model path depends on.

**[#39123](https://github.com/sgl-project/sglang/pull/39123) [DSV4.1] Paged KV cache layouts for FlashMLA's V4.1 fp8 / fp4 formats**
Adds paged KV layouts for FlashMLA's V4.1 fp8 and fp4 formats, so V4.1 can run with a quantized KV cache. Paired with the FlashMLA fork bump in [#39171](https://github.com/sgl-project/sglang/pull/39171).

**[#36729](https://github.com/sgl-project/sglang/pull/36729) Use a shared byte budget for unified hybrid-SWA memory**
Replaces per-pool sizing with one shared byte budget across the unified hybrid sliding-window-attention pools, so memory can flow between pools. Related unified-memory PRs ([#37418](https://github.com/sgl-project/sglang/pull/37418) prefill CUDA graph, [#37506](https://github.com/sgl-project/sglang/pull/37506) PD) landed too.

**[#30775](https://github.com/sgl-project/sglang/pull/30775) Pipeline parallelism x speculative decoding (EAGLE/MTP)**
Makes PP compatible with EAGLE/MTP drafting, which previously could not be combined. Follow-ups such as [#39643](https://github.com/sgl-project/sglang/pull/39643) and [#39885](https://github.com/sgl-project/sglang/pull/39885) are open.

## More changes by area

<details>
<summary>Performance (6)</summary>

- [#39050](https://github.com/sgl-project/sglang/pull/39050) batch HiCache D2H submits per step for hybrid pools
- [#39232](https://github.com/sgl-project/sglang/pull/39232) trtllm_mla reuses the fused fp8 KV/Q prepare on target verify
- [#39445](https://github.com/sgl-project/sglang/pull/39445) DSV4.1 multi-stream prepare, fused ratio-1 verify compression, PDL on _q_rope_store
- [#39674](https://github.com/sgl-project/sglang/pull/39674) DSV4.1 native 16-head attention for small TP4 decode batches
- [#39480](https://github.com/sgl-project/sglang/pull/39480) optimize buffer-mode storage existence bookkeeping
- [#39813](https://github.com/sgl-project/sglang/pull/39813) fail fast and speed up NPU qwen3.6 accuracy cases

</details>

<details>
<summary>Kernels & attention (13)</summary>

- [#39665](https://github.com/sgl-project/sglang/pull/39665) dsv4.1 chat encoding and tool parsing
- [#39664](https://github.com/sgl-project/sglang/pull/39664) dsv4.1 mHC computation and compensated projections
- [#39671](https://github.com/sgl-project/sglang/pull/39671) dsv4.1 candidate indexer library
- [#39305](https://github.com/sgl-project/sglang/pull/39305) exact bf16 consumer top-k adapted from DeepSelect
- [#39666](https://github.com/sgl-project/sglang/pull/39666) dsv4.1 Engram module and request history support
- [#39668](https://github.com/sgl-project/sglang/pull/39668) dsv4.1 vision tower and image preprocessing
- [#39677](https://github.com/sgl-project/sglang/pull/39677) dsv4.1 Rust extension modules for image preprocessing, KV pool names, and PD bootstrap
- [#36821](https://github.com/sgl-project/sglang/pull/36821) KDA ReplaySSM ring-write in the fused chain-verify kernel
- [#39172](https://github.com/sgl-project/sglang/pull/39172) gfx950 assembly attention: length-aware split-KV
- [#38584](https://github.com/sgl-project/sglang/pull/38584) optimize Qwen-Image-Edit attention on Hopper
- [#33426](https://github.com/sgl-project/sglang/pull/33426) make the FlashAttention backend extensible by subclasses
- [#39219](https://github.com/sgl-project/sglang/pull/39219) don't write conv state from the fused KDA verify kernel
- [#38687](https://github.com/sgl-project/sglang/pull/38687) OOT dispatch for clamp position

</details>

<details>
<summary>MoE & quantization (12)</summary>

- [#39414](https://github.com/sgl-project/sglang/pull/39414) NVLink collectives and the DSpark draft head's vocab gather
- [#39374](https://github.com/sgl-project/sglang/pull/39374) Kimi K3 2xB300 EP16 optimization stack
- [#38160](https://github.com/sgl-project/sglang/pull/38160) BF16 and batch-invariant inference with DeepEP v2
- [#38913](https://github.com/sgl-project/sglang/pull/38913) H20 block-FP8 MoE configs for GLM-5.3-Flash EP4/EP8
- [#39155](https://github.com/sgl-project/sglang/pull/39155) GLM-5.2 NextN: cast draft fused MoE to per-channel FP8
- [#39126](https://github.com/sgl-project/sglang/pull/39126) Qwen3.8 NVFP4 on DGX Spark with file-backed PLE
- [#39089](https://github.com/sgl-project/sglang/pull/39089) back up MXFP8 KV scales in the host pool
- [#39223](https://github.com/sgl-project/sglang/pull/39223) fix MegaMoE buffer allocation for effective SM budgets
- [#39613](https://github.com/sgl-project/sglang/pull/39613) accept MXFP8 dispatch in FlashInfer A2A TRT-LLM MoE
- [#28723](https://github.com/sgl-project/sglang/pull/28723) fused_moe_triton tuning on XPU
- [#35605](https://github.com/sgl-project/sglang/pull/35605) torch scaled_mm for XPU block FP8 linear
- [#32618](https://github.com/sgl-project/sglang/pull/32618) fp8_per_tensor_scaled_mm_cpu kernel

</details>

<details>
<summary>Model support (7)</summary>

- [#38526](https://github.com/sgl-project/sglang/pull/38526) Ling-3.0-flash-VL
- [#38890](https://github.com/sgl-project/sglang/pull/38890) non-strict GLM47 tool calls with EBNF constraints
- [#39227](https://github.com/sgl-project/sglang/pull/39227) force reasoning mode for GLM-5.3 chat templates
- [#36576](https://github.com/sgl-project/sglang/pull/36576) MiniMax-M3 shared-experts fusion on ROCm gfx942+
- [#38878](https://github.com/sgl-project/sglang/pull/38878) fused shared experts for Qwen4-Exp and Qwen3.5 MTP on AMD
- [#38176](https://github.com/sgl-project/sglang/pull/38176) keep router GEMM in fp32 for deterministic DeepSeek V3/V4
- [#39278](https://github.com/sgl-project/sglang/pull/39278) normalize the Qwen-VL image sentinel on the artifact fast path

</details>

<details>
<summary>Parallelism & scheduling (16)</summary>

- [#39283](https://github.com/sgl-project/sglang/pull/39283) HiCache buffer-mode prefetch pipeline and retry rework
- [#39318](https://github.com/sgl-project/sglang/pull/39318) scope prefetch cache state to the request attempt
- [#37615](https://github.com/sgl-project/sglang/pull/37615) kv-shard 2/4 sharded pools
- [#37482](https://github.com/sgl-project/sglang/pull/37482) attribute stored KV cache blocks to sessions
- [#34012](https://github.com/sgl-project/sglang/pull/34012) agentic-aware tail-optimized LRU eviction in the unified radix cache
- [#37418](https://github.com/sgl-project/sglang/pull/37418) unified-memory prefill CUDA graph capture
- [#37506](https://github.com/sgl-project/sglang/pull/37506) PD disaggregation for every unified pool shape
- [#39500](https://github.com/sgl-project/sglang/pull/39500) optional KV transfer checksums in PD
- [#38935](https://github.com/sgl-project/sglang/pull/38935) don't admit intake-rejected requests to a PD handoff
- [#39332](https://github.com/sgl-project/sglang/pull/39332) gate PD decode admission on LoRA adapter slots
- [#36141](https://github.com/sgl-project/sglang/pull/36141) /v1/responses on the HTTP PD router
- [#39182](https://github.com/sgl-project/sglang/pull/39182) provider hook for prefill-buffer ceilings
- [#39202](https://github.com/sgl-project/sglang/pull/39202) delete the redundant full stamp in initialize_model_parallel
- [#39137](https://github.com/sgl-project/sglang/pull/39137) delete dead ensure_model_parallel_initialized
- [#39134](https://github.com/sgl-project/sglang/pull/39134) out-of-tree replacement point for every config resolution step
- [#37914](https://github.com/sgl-project/sglang/pull/37914) MTP/EAGLE/DSpark draft KV caches in the external linker

</details>

<details>
<summary>Hardware & arch (15)</summary>

- [#37413](https://github.com/sgl-project/sglang/pull/37413) AMD DSV4 fp8 two-pool unified_kv on gfx950
- [#37810](https://github.com/sgl-project/sglang/pull/37810) ROCm DSV4 breakable CUDA graph prefill
- [#39551](https://github.com/sgl-project/sglang/pull/39551) multi-arch ROCm support for internal testing
- [#37134](https://github.com/sgl-project/sglang/pull/37134) fix ROCm EAGLE verify silently sampling greedy
- [#38184](https://github.com/sgl-project/sglang/pull/38184) GDN ReplaySSM target-verify on ROCm
- [#39631](https://github.com/sgl-project/sglang/pull/39631) prefer HIP Top-K for GLM-5.x on ROCm
- [#37382](https://github.com/sgl-project/sglang/pull/37382) NPU DSV4 host memory cache management
- [#39427](https://github.com/sgl-project/sglang/pull/39427) NPU DSV4 prefill context parallelism (interleave and zigzag)
- [#38420](https://github.com/sgl-project/sglang/pull/38420) NPU weight processing refactor and NPUSwigluLimit activation
- [#32500](https://github.com/sgl-project/sglang/pull/32500) HiCache Ascend Mamba states with FIA and async IO
- [#39438](https://github.com/sgl-project/sglang/pull/39438) NPU diffusion FA MXFP8 and w4a4f8/w8a8f8 for Wan2.2 and FLUX
- [#39382](https://github.com/sgl-project/sglang/pull/39382) NPU SenseNova-U1 batched generation
- [#39404](https://github.com/sgl-project/sglang/pull/39404) avoid device sync in Ascend sampling
- [#36472](https://github.com/sgl-project/sglang/pull/36472) base NpuSRTPlatform
- [#39439](https://github.com/sgl-project/sglang/pull/39439) XPU weekly simple model enablement

</details>

<details>
<summary>API & serving (22)</summary>

- [#39457](https://github.com/sgl-project/sglang/pull/39457) sgl-router dynamo-render dependencies
- [#38983](https://github.com/sgl-project/sglang/pull/38983) render chat prompts with dynamo-render
- [#39168](https://github.com/sgl-project/sglang/pull/39168) router --worker-queue-limit
- [#39169](https://github.com/sgl-project/sglang/pull/39169) router pin to the prefix owner when the fleet is queueing
- [#39108](https://github.com/sgl-project/sglang/pull/39108) honor KV-event storage tiers in the cache-aware tree
- [#39109](https://github.com/sgl-project/sglang/pull/39109) expose KV storage-tier stream and tree occupancy on /metrics
- [#39110](https://github.com/sgl-project/sglang/pull/39110) real-GPU e2e coverage for tier-aware routing
- [#39111](https://github.com/sgl-project/sglang/pull/39111) Grafana KV storage-tier row
- [#39000](https://github.com/sgl-project/sglang/pull/39000) fleet-wide sampling contract 1/3
- [#39001](https://github.com/sgl-project/sglang/pull/39001) fleet-wide sampling contract 2/3
- [#39002](https://github.com/sgl-project/sglang/pull/39002) fleet-wide sampling contract 3/3
- [#39016](https://github.com/sgl-project/sglang/pull/39016) drain readiness before SIGTERM
- [#39015](https://github.com/sgl-project/sglang/pull/39015) shutdown-drain configuration surface
- [#39006](https://github.com/sgl-project/sglang/pull/39006) cleartext h2c on both edges
- [#39004](https://github.com/sgl-project/sglang/pull/39004) resolve wire protocol per worker at registration
- [#39329](https://github.com/sgl-project/sglang/pull/39329) external multimodal processors in the Rust frontend
- [#39122](https://github.com/sgl-project/sglang/pull/39122) gate /v1/responses persistence behind --enable-response-store
- [#37488](https://github.com/sgl-project/sglang/pull/37488) expose native pause status over gRPC
- [#39863](https://github.com/sgl-project/sglang/pull/39863) cherry-pick of [#37488](https://github.com/sgl-project/sglang/pull/37488)
- [#38737](https://github.com/sgl-project/sglang/pull/38737) stream outcome observability for 2xx SSE streams
- [#39014](https://github.com/sgl-project/sglang/pull/39014) count open HTTP exchanges until response body finishes
- plus 4 more minor router/frontend changes ([#39322](https://github.com/sgl-project/sglang/pull/39322), [#39458](https://github.com/sgl-project/sglang/pull/39458), [#39459](https://github.com/sgl-project/sglang/pull/39459), [#38939](https://github.com/sgl-project/sglang/pull/38939))

</details>

<details>
<summary>Bugfixes (24)</summary>

- [#39136](https://github.com/sgl-project/sglang/pull/39136) preserve GLM tool argument types across JSON Schema unions
- [#37839](https://github.com/sgl-project/sglang/pull/37839) prevalidate JSON Schema support per grammar backend
- [#39869](https://github.com/sgl-project/sglang/pull/39869) allow closed object schemas in Outlines prevalidation
- [#39574](https://github.com/sgl-project/sglang/pull/39574) fix tool-call index, graph padded-row count, prefill-graph input_embeds refresh
- [#39487](https://github.com/sgl-project/sglang/pull/39487) localize widened KV ids in DCP MLA retraction backup/restore
- [#38941](https://github.com/sgl-project/sglang/pull/38941) merge adjacent KV-row frees to avoid double-free under DCP
- [#35233](https://github.com/sgl-project/sglang/pull/35233) fix registered HiCache host pointer aliases on AMD
- [#31926](https://github.com/sgl-project/sglang/pull/31926) fix silent Mooncake SSD offload corruption
- [#29668](https://github.com/sgl-project/sglang/pull/29668) resolve Mooncake local_hostname per node
- [#38503](https://github.com/sgl-project/sglang/pull/38503) fix Mooncake scale joiners
- [#39516](https://github.com/sgl-project/sglang/pull/39516) fix HiCache startup ImportError
- [#39699](https://github.com/sgl-project/sglang/pull/39699) keep hybrid transfer layer maps stage-local under PP
- [#39560](https://github.com/sgl-project/sglang/pull/39560) release NCCL on scheduler exit
- [#38774](https://github.com/sgl-project/sglang/pull/38774) fix device context in NIXL init
- [#38402](https://github.com/sgl-project/sglang/pull/38402) fix NPU hybrid KV transfer with PP prefill
- [#39115](https://github.com/sgl-project/sglang/pull/39115) fix Mamba checkpoint depth for off-page prefixes
- [#39145](https://github.com/sgl-project/sglang/pull/39145) fix session image append positions
- [#39038](https://github.com/sgl-project/sglang/pull/39038) session: work with PD and fix empty continuations
- [#39120](https://github.com/sgl-project/sglang/pull/39120) fix multimodal embedding cache retaining batches via views
- [#39237](https://github.com/sgl-project/sglang/pull/39237) fix /model_info serialization when a config value is a class
- [#39513](https://github.com/sgl-project/sglang/pull/39513) fix vattn_asm HIP error 709 under CUDA graph capture
- [#37564](https://github.com/sgl-project/sglang/pull/37564) fix aiter bpreshuffle GEMM dispatch for Qwen3.5 mxfp-attn-fp8-v2 TP4
- [#39875](https://github.com/sgl-project/sglang/pull/39875) fix AMD dsv4 server launch
- [#39328](https://github.com/sgl-project/sglang/pull/39328) fix first-token metadata and attention-layer indexing

</details>

<details>
<summary>Tests (12)</summary>

- [#39835](https://github.com/sgl-project/sglang/pull/39835) re-land dp-attention local control broadcast test
- [#39437](https://github.com/sgl-project/sglang/pull/39437) e2e test for dp-attention local control broadcast
- [#39828](https://github.com/sgl-project/sglang/pull/39828) revert of [#39437](https://github.com/sgl-project/sglang/pull/39437)
- [#39544](https://github.com/sgl-project/sglang/pull/39544) trim redundant variants from the 8-gpu-h20 disaggregation suite
- [#39584](https://github.com/sgl-project/sglang/pull/39584) give prefill and decode their own RDMA NICs in disaggregation tests
- [#39611](https://github.com/sgl-project/sglang/pull/39611) fix EADDRINUSE flake in the dwdp gpt_oss test
- [#39713](https://github.com/sgl-project/sglang/pull/39713) bound the router e2e worker memory budget
- [#37015](https://github.com/sgl-project/sglang/pull/37015) unit test for muse_glimmer_format
- [#39906](https://github.com/sgl-project/sglang/pull/39906) unify sanity accuracy checks with MMLU
- [#39874](https://github.com/sgl-project/sglang/pull/39874) LongBench v2 in one-batch server benchmarks
- [#39545](https://github.com/sgl-project/sglang/pull/39545) wait for a killed test server's GPU memory
- [#34981](https://github.com/sgl-project/sglang/pull/34981) split model-loader weight loading from postprocessing

</details>

<details>
<summary>CI & build (9)</summary>

- [#38632](https://github.com/sgl-project/sglang/pull/38632) consolidate AMD workflows, retire ROCm 7.0 CI
- [#38833](https://github.com/sgl-project/sglang/pull/38833) NPU CANN 9.1.0 and Ascend a5 nightly suites
- [#39697](https://github.com/sgl-project/sglang/pull/39697) fix always-failing coverage job
- [#39892](https://github.com/sgl-project/sglang/pull/39892) fix sanity evaluation and diffusion suite blockers
- [#39371](https://github.com/sgl-project/sglang/pull/39371) bump sgl-deep-gemm to 0.2.0
- [#39241](https://github.com/sgl-project/sglang/pull/39241) fix DeepGEMM release dependencies
- [#39796](https://github.com/sgl-project/sglang/pull/39796) nightly XPU docker build can target a branch or tag
- [#39255](https://github.com/sgl-project/sglang/pull/39255) diffusion GT generation without publish token
- plus 3 more minor NPU CI updates ([#39403](https://github.com/sgl-project/sglang/pull/39403), [#39585](https://github.com/sgl-project/sglang/pull/39585), [#39813](https://github.com/sgl-project/sglang/pull/39813) excluded above)

</details>

<details>
<summary>Docs (6)</summary>

- [#39389](https://github.com/sgl-project/sglang/pull/39389) rename NPU hardware to Ascend A2/A3 Series
- [#39396](https://github.com/sgl-project/sglang/pull/39396) DeepSeek-V4 MI355X PD disaggregation recipes
- [#39244](https://github.com/sgl-project/sglang/pull/39244) refresh MiniMax-H3 cookbook B200 numbers
- [#39373](https://github.com/sgl-project/sglang/pull/39373) RTX 5090 H3 recipe
- [#39252](https://github.com/sgl-project/sglang/pull/39252) AMD dspark config and agentic workload for deepseek-v4
- [#39702](https://github.com/sgl-project/sglang/pull/39702) AMD deepseek-v4 PDI and cache policy settings

</details>

<details>
<summary>Refactors (4)</summary>

- [#39295](https://github.com/sgl-project/sglang/pull/39295) clean up no-op compiler pass, dead helpers, migration tests
- [#39293](https://github.com/sgl-project/sglang/pull/39293) clean up obsolete diffusion worker plumbing
- [#35644](https://github.com/sgl-project/sglang/pull/35644) drop the redundant _component suffix in unified_cache/components
- [#39405](https://github.com/sgl-project/sglang/pull/39405) revert #38346, [#33426](https://github.com/sgl-project/sglang/pull/33426), [#39061](https://github.com/sgl-project/sglang/pull/39061) and [#39219](https://github.com/sgl-project/sglang/pull/39219)

</details>

<details>
<summary>Other (~35)</summary>

- [#39459](https://github.com/sgl-project/sglang/pull/39459) rename chat encoder to chat formatter (counted under API above)
- [#39358](https://github.com/sgl-project/sglang/pull/39358) AMD Qwen3.5 MI355X cookbook alignment
- [#39406](https://github.com/sgl-project/sglang/pull/39406) AMD GLM-5.2 MI355X MXFP4 image bump and TOPK_V2
- [#39555](https://github.com/sgl-project/sglang/pull/39555) delete unsupported models in NPU docs
- [#39858](https://github.com/sgl-project/sglang/pull/39858) restrict SafeUnpickler standard-library globals
- [#34712](https://github.com/sgl-project/sglang/pull/34712) spawn, don't fork, the benchmark server
- [#38630](https://github.com/sgl-project/sglang/pull/38630) label draft and verify steps in profiler spans
- [#35802](https://github.com/sgl-project/sglang/pull/35802) custom OTLP trace service name
- [#38657](https://github.com/sgl-project/sglang/pull/38657) explicit x264 preset for diffusion video output
- [#39882](https://github.com/sgl-project/sglang/pull/39882) preserve explicit attention backends during autotune
- [#39291](https://github.com/sgl-project/sglang/pull/39291) make the SP sequence gather pass contiguous shards
- [#39303](https://github.com/sgl-project/sglang/pull/39303) serve CFG-off requests on a CFG-parallel server
- [#38549](https://github.com/sgl-project/sglang/pull/38549) return Qwen-Image-Layered outputs
- [#33452](https://github.com/sgl-project/sglang/pull/33452) CPU fused scale-shift and norm kernels for diffusion
- [#37748](https://github.com/sgl-project/sglang/pull/37748) CPU fused QK Norm and RoPE kernels
- [#39870](https://github.com/sgl-project/sglang/pull/39870) carry deferred attention operands and reuse multimodal shared memory
- [#39164](https://github.com/sgl-project/sglang/pull/39164) generalize auxiliary outputs
- [#39178](https://github.com/sgl-project/sglang/pull/39178) capacity check for graph-pool borrows
- [#39180](https://github.com/sgl-project/sglang/pull/39180) keep graph-pool borrows on their allocation stream
- [#39567](https://github.com/sgl-project/sglang/pull/39567) forward prefix metadata to v2 storage calls
- [#39162](https://github.com/sgl-project/sglang/pull/39162) simplify HiCache LoRA decode offload hash inputs
- [#39280](https://github.com/sgl-project/sglang/pull/39280) label radix-cache metrics per rank
- [#38486](https://github.com/sgl-project/sglang/pull/38486) publish a host store event for storage-prefetch refills
- [#38483](https://github.com/sgl-project/sglang/pull/38483) release buffer prefetch anchor locks during storage cleanup
- [#37425](https://github.com/sgl-project/sglang/pull/37425) HiCache rank_consensus on various functions
- [#39485](https://github.com/sgl-project/sglang/pull/39485) share model-file discovery for chat formatters
- [#31804](https://github.com/sgl-project/sglang/pull/31804) EPLB drop defensive getattr
- [#37474](https://github.com/sgl-project/sglang/pull/37474) gate mamba extra-buffer predicates
- [#38554](https://github.com/sgl-project/sglang/pull/38554) let speculative workers stage prefill shared reads
- [#39678](https://github.com/sgl-project/sglang/pull/39678) merge FlashInfer autotune caches across spec workers
- [#32888](https://github.com/sgl-project/sglang/pull/32888) fill chunked-prefill compute budget exactly on gfx95
- [#39426](https://github.com/sgl-project/sglang/pull/39426) fix unifiedcache c128 radix cache management
- [#38453](https://github.com/sgl-project/sglang/pull/38453) avoid FP8 wo_a path when weight is BF16
- [#39292](https://github.com/sgl-project/sglang/pull/39292) don't route an unreadable checkpoint into native fallback
- #39236 not applicable; plus ~49 more small merged PRs not listed in the data

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (sglang.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: 66b8700f0cf73259fc699efa20f3255205002e2c187765891a47be36304dd377 -->
