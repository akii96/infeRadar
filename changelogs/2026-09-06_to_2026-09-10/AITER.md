# AITER: PR digest (2026-09-06 to 2026-09-10)

_65 merged, 58 newly opened - source ROCm/AITER, generated 2026-09-10T13:22:19Z_

## TL;DR
- **Model attention:** DeepSeek (V4 / DSv4, 12 PRs) and Kimi (K3, 9) led, followed by GLM, Qwen3.8 and MiniMax-M3. The work is mostly tuned GEMM and MoE configs plus kernel fixes. Qwen3.8-Flash-Next got large FP8 PTPC and BF16 MoE tuning ([#5213](https://github.com/ROCm/aiter/pull/5213)). Kimi got low-M MXFP4 fused-MoE and a16wi4 work ([#5300](https://github.com/ROCm/aiter/pull/5300), [#5240](https://github.com/ROCm/aiter/pull/5240)).
- **Performance:** FlyDSL is the center of gravity. Merged work includes FP8 flash attention on gfx950 ([#5326](https://github.com/ROCm/aiter/pull/5326)), a8w8 gather-GEMM ([#5207](https://github.com/ROCm/aiter/pull/5207)) and the mega_moe fused path ([#5001](https://github.com/ROCm/aiter/pull/5001), though it was reverted and restored). The new Gluon MHA kernel ([#4147](https://github.com/ROCm/aiter/pull/4147)) and the MHA v4 rework ([#5335](https://github.com/ROCm/aiter/pull/5335)) also landed.
- **gfx1250 push:** DSv4 narrow-head MLA sparse-prefill kernels ([#5228](https://github.com/ROCm/aiter/pull/5228)), split-K fixes ([#5162](https://github.com/ROCm/aiter/pull/5162)), tuning for DeepSeek-R1 GEMMs ([#5349](https://github.com/ROCm/aiter/pull/5349)) and many benchmark and microbench PRs.
- **In flight:** FP8/FP4 LiteTopK prefill ([#5348](https://github.com/ROCm/aiter/pull/5348), [#5309](https://github.com/ROCm/aiter/pull/5309)), FP8 sparse MLA on gfx950 ([#5301](https://github.com/ROCm/aiter/pull/5301)), ragged MXFP4 grouped GEMM ([#5389](https://github.com/ROCm/aiter/pull/5389)) and Triton/Gluon MoE GEMM and weight-gradient kernels for training. Direction is DSv4 / Kimi-K3 enablement and consolidating the kernel backends.

## Most important PRs
**[#5326](https://github.com/ROCm/aiter/pull/5326) FlyDSL FP8 flash attention for gfx950.** Adds dense, asymmetric-head-dim, varlen and KV-split FP8 attention. This is a major new attention path, and the follow-up fixes ([#5364](https://github.com/ROCm/aiter/pull/5364), and [#5405](https://github.com/ROCm/aiter/pull/5405) still open) show it is being hardened.

**[#5001](https://github.com/ROCm/aiter/pull/5001) / [#5346](https://github.com/ROCm/aiter/pull/5346) / [#5345](https://github.com/ROCm/aiter/pull/5345) mega_moe stage1 and AOT bundles.** The fused stage1 optimization and AOT bundles landed, were reverted ([#5345](https://github.com/ROCm/aiter/pull/5345)), then restored with an AOT fix ([#5346](https://github.com/ROCm/aiter/pull/5346)). It is a ~7k-line churn on the fused MoE-plus-communication path.

**[#4985](https://github.com/ROCm/aiter/pull/4985) FlyDSL comm fused MoE with JIT and CI.** Adds a distributed fused MoE path with communication kernels, tuning configs and CI for gfx950, tagged DeepSeek. This is the multi-GPU MoE building block.

**[#5335](https://github.com/ROCm/aiter/pull/5335) MHA v4 across Triton, Gluon, ASM and HIP.** Adds a new kernel, fixes, a refactor and perf tweaks for gfx950. It sits alongside the new Gluon MHA kernel ([#4147](https://github.com/ROCm/aiter/pull/4147)).

**[#5300](https://github.com/ROCm/aiter/pull/5300) Low-M MXFP4 fused MoE.** Bounds the launch to padded rows, fuses SiTUv2 stage1 and adds BM16 inline-sort. This targets the small-batch decode latency of Kimi.

## More changes by area

<details>
<summary>Performance (9)</summary>

- [#5216](https://github.com/ROCm/aiter/pull/5216) optimize FP8 MQA logits Gluon kernel on MI350
- [#4761](https://github.com/ROCm/aiter/pull/4761) optimize Triton unified attention prefill and decode
- [#5285](https://github.com/ROCm/aiter/pull/5285) bound the FP4 MQA-logits store with a window-sized V# (DSv4)
- [#5305](https://github.com/ROCm/aiter/pull/5305) large-M/small-N RMSNorm backward specialization
- [#5304](https://github.com/ROCm/aiter/pull/5304) label SMI replays per benchmark call on gfx1250
- [#5323](https://github.com/ROCm/aiter/pull/5323) use tuned paths in gfx1250 combo benchmarks
- [#5302](https://github.com/ROCm/aiter/pull/5302) reuse process-wide amdsmi state
- [#5373](https://github.com/ROCm/aiter/pull/5373) gfx1250 hca_compress optimization (open)
- [#5313](https://github.com/ROCm/aiter/pull/5313) speed up gfx1250 grouped-MoE route, quant and gather-reduce epilogues (open)

</details>

<details>
<summary>Kernels & attention (23)</summary>

- [#4441](https://github.com/ROCm/aiter/pull/4441) FlyDSL HSTU forward kernel
- [#5165](https://github.com/ROCm/aiter/pull/5165) vocab-parallel cross-entropy kernel
- [#5207](https://github.com/ROCm/aiter/pull/5207) is listed above under the FlyDSL gather-GEMM entry
- [#5280](https://github.com/ROCm/aiter/pull/5280) add rowcol_wp_v2 selectable cktile a8w8-bpreshuffle kernel
- [#5214](https://github.com/ROCm/aiter/pull/5214) mla decode kernel name prefix
- [#5359](https://github.com/ROCm/aiter/pull/5359) designated initializers for FMHA forward arguments
- [#5367](https://github.com/ROCm/aiter/pull/5367) rebuild gfx1250 mla v4 sparse_pfl kernel
- [#5348](https://github.com/ROCm/aiter/pull/5348) FP8 LiteTopK prefill operator (open)
- [#5309](https://github.com/ROCm/aiter/pull/5309) FP4 LiteTopK prefill operator (open)
- [#5405](https://github.com/ROCm/aiter/pull/5405) runtime softmax scale in gfx950 FP8 FMHA (open)
- [#5301](https://github.com/ROCm/aiter/pull/5301) gfx950 FP8 sparse MLA prefill and decode in FlyDSL (open)
- [#5332](https://github.com/ROCm/aiter/pull/5332) OPUS PA MQA Logits MXFP4 (open)
- [#5363](https://github.com/ROCm/aiter/pull/5363) radix topk one block (open)
- [#5347](https://github.com/ROCm/aiter/pull/5347) manifest-driven static-page batch prefill dispatch (open)
- [#5403](https://github.com/ROCm/aiter/pull/5403) bf16 hd=256 forward ASM kernel for gfx950 (open)
- [#5376](https://github.com/ROCm/aiter/pull/5376) bf16 hd=256 fused dKdV+dQ ASM backward kernels (open)
- [#5389](https://github.com/ROCm/aiter/pull/5389) ragged MXFP4 grouped GEMM and wgrad (open)
- [#5358](https://github.com/ROCm/aiter/pull/5358) a6w4 preshuffle GEMM from FlyDSL (open)
- [#5362](https://github.com/ROCm/aiter/pull/5362) gfx950 split Softmax and FP32 split-K BF16 GEMM (open)
- [#5370](https://github.com/ROCm/aiter/pull/5370) Conv3d for Qwen-Image / Wan2.1 VAE (open)
- [#5397](https://github.com/ROCm/aiter/pull/5397) opus gemm 256tile ring (open)
- [#5400](https://github.com/ROCm/aiter/pull/5400) FP8 output in gather_kv_b_proj (open)
- [#5402](https://github.com/ROCm/aiter/pull/5402) rebuild 7 gfx1250 MLA decode kernels with missing SCHED_MODE (open)

</details>

<details>
<summary>MoE & quantization (21)</summary>

- [#5213](https://github.com/ROCm/aiter/pull/5213) tuned FP8 PTPC and BF16 MoE configs for Qwen3.8-Flash-Next
- [#5240](https://github.com/ROCm/aiter/pull/5240) opt-in a16wi4 gemm2 CShuffle epilog
- [#5203](https://github.com/ROCm/aiter/pull/5203) MXFP8 convert and fast-transpose kernels
- [#5177](https://github.com/ROCm/aiter/pull/5177) FP8 block-wise quantization kernels
- [#5317](https://github.com/ROCm/aiter/pull/5317) migrate mixed MoE 2-stage LDS to fly shared storage
- [#5275](https://github.com/ROCm/aiter/pull/5275) tuned bf16 MoE for K2 horizon 375B
- [#5255](https://github.com/ROCm/aiter/pull/5255) reject non-int32 index buffers in topk kernels
- [#5271](https://github.com/ROCm/aiter/pull/5271) stop the reference clamping SwiGLU at swiglu_limit=0
- [#5357](https://github.com/ROCm/aiter/pull/5357) 64-bit weight offsets in ASM MoE
- [#5310](https://github.com/ROCm/aiter/pull/5310) MoE GEMM variants and weight-gradient kernel (open)
- [#5338](https://github.com/ROCm/aiter/pull/5338) per-token-scaled grouped MoE GEMM (open)
- [#5339](https://github.com/ROCm/aiter/pull/5339) MoE weight-gradient kernel (open)
- [#5355](https://github.com/ROCm/aiter/pull/5355) Gluon MoE A16W4 gfx950 kernels (open)
- [#5398](https://github.com/ROCm/aiter/pull/5398) split layout-v2 MoE GEMM2 into mxmoe_g2 (open)
- [#5321](https://github.com/ROCm/aiter/pull/5321) Kimi-K3 merged MoE front (open)
- [#5404](https://github.com/ROCm/aiter/pull/5404) BM16 SwiGLU path for MiniMax M3 (open)
- [#5395](https://github.com/ROCm/aiter/pull/5395) enable SwiGLU and tune MiniMax-M3 A16W4 MoE (open)
- [#5392](https://github.com/ROCm/aiter/pull/5392) optional sigmoid on gated_rmsnorm_fp8_per_token_quant (open)
- [#5388](https://github.com/ROCm/aiter/pull/5388) tune 16x128 mxfp4 kernel (open)
- [#5379](https://github.com/ROCm/aiter/pull/5379) Qwen3.8 Flash Next FP8 prefill config on MI308X (open)
- [#5368](https://github.com/ROCm/aiter/pull/5368) draft: Kimi K3 a8w4 MoE TP8 config (open)

</details>

<details>
<summary>Model support & tuning configs (17)</summary>

- [#5343](https://github.com/ROCm/aiter/pull/5343) GLM-5.3-Flash a8w8 blockscale GEMM configs for gfx942
- [#5328](https://github.com/ROCm/aiter/pull/5328) tune GLM-5.2 decode shapes on gfx950
- [#5360](https://github.com/ROCm/aiter/pull/5360) Kimi-K3 a8w8 bpreshuffle long-prefill tuning
- [#5349](https://github.com/ROCm/aiter/pull/5349) DSR1 Triton GEMM tuning on gfx1250
- [#5283](https://github.com/ROCm/aiter/pull/5283) DSv4 FP8 blockscale tuning for wq_b / wqkv_a
- [#5279](https://github.com/ROCm/aiter/pull/5279) DSV4 wo_b/wq_b a8w8 blockscale configs
- [#5371](https://github.com/ROCm/aiter/pull/5371) retune gpt-oss N=2880,K=4096 off hipBLASLt for CUDAGraph capture
- [#5246](https://github.com/ROCm/aiter/pull/5246) Conv2D configs for gfx1101 and gfx1150
- [#5249](https://github.com/ROCm/aiter/pull/5249) chunk_kimi_delta_attn accepts non-fp32 KDA state
- [#5353](https://github.com/ROCm/aiter/pull/5353) modify kimik3_bf16_tuned_gemm.csv (open)
- [#5350](https://github.com/ROCm/aiter/pull/5350) Qwen3.8-27B MXFP4 configs (open)
- [#5378](https://github.com/ROCm/aiter/pull/5378) GLM-5.2 native-MTP M=4 projections (open)
- [#5377](https://github.com/ROCm/aiter/pull/5377) MiniMax-M3 MXFP4 shared-expert down_proj config (open)
- [#5399](https://github.com/ROCm/aiter/pull/5399) fix ff_a16w16_fused M<=8 launch, add configs (open)
- [#5333](https://github.com/ROCm/aiter/pull/5333) gfx1100 tune (open)
- [#5406](https://github.com/ROCm/aiter/pull/5406) gfx1250 a8w8 mxfp8_128 GEMM A-preshuffle and fused split-k (open)
- [#5315](https://github.com/ROCm/aiter/pull/5315) explicit gfx in shipped fused-MoE tuning CSVs (open)

</details>

<details>
<summary>Parallelism & scheduling (1)</summary>

- [#5129](https://github.com/ROCm/aiter/pull/5129) move all2all tuning config file

</details>

<details>
<summary>Hardware & arch (4)</summary>

- [#5162](https://github.com/ROCm/aiter/pull/5162) gfx1250 split-K off shapes its reduce cannot address
- [#5311](https://github.com/ROCm/aiter/pull/5311) add --combine both to gfx1250 mega_moe ubench
- [#5391](https://github.com/ROCm/aiter/pull/5391) gfx1250 microbench (open)
- [#5361](https://github.com/ROCm/aiter/pull/5361) MI355X gfx950 dense-operator benchmarks (open)

</details>

<details>
<summary>API & serving (3)</summary>

- [#5287](https://github.com/ROCm/aiter/pull/5287) rewrite gfx950 HGEMM test to op_test standard
- [#5340](https://github.com/ROCm/aiter/pull/5340) gfx:cu_num build targets so one build serves multiple SKUs (open)
- [#5342](https://github.com/ROCm/aiter/pull/5342) bake only the FlyDSL GEMM kernels a build's targets can run (open)

</details>

<details>
<summary>Tests (3)</summary>

- [#5289](https://github.com/ROCm/aiter/pull/5289) review-pr gates and evidence from 200 PRs
- [#5308](https://github.com/ROCm/aiter/pull/5308) validate-kernel-pr skill: prose for judgement, code for the ledger (open)
- [#5390](https://github.com/ROCm/aiter/pull/5390) suppress aiter logger under pytest (open)

</details>

<details>
<summary>CI & build (6)</summary>

- [#5312](https://github.com/ROCm/aiter/pull/5312) stop stamping torch-free modules with torch's pybind11 ABI identity
- [#5318](https://github.com/ROCm/aiter/pull/5318) fix auditwheel excludes that grafted ~890MB into the wheel
- [#5365](https://github.com/ROCm/aiter/pull/5365) fix cpu isolation vs sglang cpu affinity conflict
- [#5382](https://github.com/ROCm/aiter/pull/5382) absolute imports under ops/triton and triton_tests
- [#5381](https://github.com/ROCm/aiter/pull/5381) absolute imports under ops/triton and triton_tests (open)
- [#5352](https://github.com/ROCm/aiter/pull/5352) fix stale MHA config-utils import

</details>

<details>
<summary>Docs (2)</summary>

- [#5369](https://github.com/ROCm/aiter/pull/5369) PR-scope, comment and UT-hygiene rules in Copilot review instructions
- [#5383](https://github.com/ROCm/aiter/pull/5383) torch-free Triton docs

</details>

<details>
<summary>Bugfixes (15)</summary>

- [#4800](https://github.com/ROCm/aiter/pull/4800) transactional blob codegen cache publication
- [#4974](https://github.com/ROCm/aiter/pull/4974) custom_all_reduce RankData slot prediction during graph capture
- [#4181](https://github.com/ROCm/aiter/pull/4181) ragged-K mask in batched A16WFP4 GEMM
- [#5261](https://github.com/ROCm/aiter/pull/5261) split-K OOB in afp4wfp4
- [#5314](https://github.com/ROCm/aiter/pull/5314) large tensor addressing in quant and inverse_rope
- [#5324](https://github.com/ROCm/aiter/pull/5324) zero GDR decode graph padding output
- [#5327](https://github.com/ROCm/aiter/pull/5327) detach tensors before DLPack conversion
- [#5329](https://github.com/ROCm/aiter/pull/5329) single-source opus half-precision dtype spellings
- [#5364](https://github.com/ROCm/aiter/pull/5364) gfx950 fp8 FMHA all-masked-tile NaN
- [#5320](https://github.com/ROCm/aiter/pull/5320) int32 overflow in Gluon paged MQA logits load offset (open)
- [#5401](https://github.com/ROCm/aiter/pull/5401) mask invalid V cache padding before PA accumulation (open)
- [#5385](https://github.com/ROCm/aiter/pull/5385) ck_batched_gemm_bf16 derives strides from tensors (open)
- [#5336](https://github.com/ROCm/aiter/pull/5336) guard FP8 MFMA kernels for gfx90a builds (open)
- [#5325](https://github.com/ROCm/aiter/pull/5325) hipBLASLt extension init resource leaks (open)
- [#5372](https://github.com/ROCm/aiter/pull/5372) Triton backward autotune dimension keys (open)

</details>

<details>
<summary>Refactors (7)</summary>

- [#5306](https://github.com/ROCm/aiter/pull/5306) remove unused gfx1250 d192 FMHA sibling kernel
- [#5303](https://github.com/ROCm/aiter/pull/5303) replace ptr_rsrc and buffer ops low-level API use
- [#4997](https://github.com/ROCm/aiter/pull/4997) move fp4 GEMM gluon to _gluon_kernels
- [#5384](https://github.com/ROCm/aiter/pull/5384) move mla_gluon kernel into _gluon_kernels/gfx950 (open)
- [#5374](https://github.com/ROCm/aiter/pull/5374) restore shared MHA backend parameterization (open)
- [#5297](https://github.com/ROCm/aiter/pull/5297) asm_mla routes ctypes failures through the error bridge (open)
- [#5341](https://github.com/ROCm/aiter/pull/5341) key opus lookup on CU count, reach gfx1250 tuned rows (open)

</details>

<details>
<summary>Other (3)</summary>

- [#5228](https://github.com/ROCm/aiter/pull/5228) narrow-head gfx1250 MLA sparse-prefill kernels for DSv4 TP (see Most important context)
- [#5393](https://github.com/ROCm/aiter/pull/5393) keep split-K preshuffle buffers out of the CUDA graph pool (open)
- [#5394](https://github.com/ROCm/aiter/pull/5394) fix HSTU reference import fallback (open)

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (AITER.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: cb28bb712046f32cb3ec321bba5d4ac24de1fc8a306b65794059bef4d8e9fc3e -->
