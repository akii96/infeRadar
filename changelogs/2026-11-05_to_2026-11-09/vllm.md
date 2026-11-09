# vllm: PR digest (2026-11-05 to 2026-11-09)

_275 merged, 421 newly opened - source vllm-project/vllm, generated 2026-11-09T00:57:38Z_

## TL;DR
- **DeepSeek V4/V4.1 and the MiniMax-M3.1 / Kimi K3.1 families got the most attention.** Work centred on sparse-MLA/DSA prefill and decode, with many ROCm MI355X "monokernel" and fused-kernel perf PRs. Gemma-4 and Qwen got smaller, targeted items.
- **Merged perf wins:**
  - Token-sharded sparse-MLA prefill under TP (`[#63956](https://github.com/vllm-project/vllm/pull/63956)`).
  - A DeepGEMM FP8 MegaMoE with fused shared experts for GLM-5.3-Flash (`[#60895](https://github.com/vllm-project/vllm/pull/60895)`).
  - An FA4 SM90 FP8 MMA path for Gemma-4 (`[#60372](https://github.com/vllm-project/vllm/pull/60372)`).
  - A cheaper DCP MLA decode merge (`[#64994](https://github.com/vllm-project/vllm/pull/64994)`).
- **Big structural change:** Model Runner V1 was deleted (`[#63373](https://github.com/vllm-project/vllm/pull/63373)`, about -40k lines), leaving MRV2 as the only runner. Alongside it, the Rust frontend gained parity features and the model loader moved toward plan-based loads (`[#65235](https://github.com/vllm-project/vllm/pull/65235)`).
- **Open pipeline:** new in-progress work includes Kimi K3.1 splits (`[#66037](https://github.com/vllm-project/vllm/pull/66037)`, `[#66027](https://github.com/vllm-project/vllm/pull/66027)`), CuTe DSL specialized decode for MiniMax-M3.1 on GB300 (`[#66324](https://github.com/vllm-project/vllm/pull/66324)`), the DSA LiteTopK prefill (`[#65920](https://github.com/vllm-project/vllm/pull/65920)`), and SM107 CuTeDSL MoE (`[#65974](https://github.com/vllm-project/vllm/pull/65974)`).

## Most important PRs
**`[#63373](https://github.com/vllm-project/vllm/pull/63373)` Remove Model Runner V1**
Deletes the legacy runner and about 40k lines across 435 files. Every backend, attention path and test now targets the V2 runner, which cuts maintenance cost and ends divergent code paths.

**`[#66030](https://github.com/vllm-project/vllm/pull/66030)` Kimi K3.1 model files and NVIDIA specialized decode (split 1/5)**
Lands the first part of Kimi K3.1 support: model code, sparse-attention and MoE kernels, and a specialized decode path on NVIDIA. Splits 3/5 and 5/5 (`[#66037](https://github.com/vllm-project/vllm/pull/66037)`, `[#66027](https://github.com/vllm-project/vllm/pull/66027)`) are still open.

**`[#63956](https://github.com/vllm-project/vllm/pull/63956)` Token-sharded sparse-MLA prefill under TP**
Shards prefill tokens across TP ranks for DSA models, which removes the replicated work and the old indexer row sharding. The result is better prefill throughput for DeepSeek-style sparse MLA.

**`[#60895](https://github.com/vllm-project/vllm/pull/60895)` DeepGEMM FP8 MegaMoE with fused shared experts (GLM-5.3-Flash)**
Fuses the shared experts into the MegaMoE kernel, so the shared and routed paths no longer run as separate launches. This is a direct MoE decode and prefill speedup.

**`[#54109](https://github.com/vllm-project/vllm/pull/54109)` DeepEPV2 PaddedStandard activation format**
Adds a padded standard activation format to the DeepEPV2 all-to-all MoE path. It broadens which expert-parallel backends and quant configs can use DeepEP.

## More changes by area

<details>
<summary>Performance (28)</summary>

- [#63027](https://github.com/vllm-project/vllm/pull/63027) tuned K1/K2 for TP2 compress-ratio-2 layers on MI355X (DSv4.1 mono)
- [#64898](https://github.com/vllm-project/vllm/pull/64898) fuse HyperConnection up-projection and gate mix for long prefills (Qwen4Exp)
- [#62702](https://github.com/vllm-project/vllm/pull/62702) keep prompt token ids as int32 buffers
- [#65227](https://github.com/vllm-project/vllm/pull/65227) encoder CUDA graphs: one replay per batch, finer grid
- [#64829](https://github.com/vllm-project/vllm/pull/64829) speed up CPU GDN speculative-decode recurrent update
- [#65478](https://github.com/vllm-project/vllm/pull/65478) fuse FFN-side MXFP8 activation quant into post-attention norm and swiglu (MiniMax-M3.1, ROCm)
- [#65267](https://github.com/vllm-project/vllm/pull/65267) opt-in parallel decode top-k (MiniMax-M3.1, ROCm)
- [#65508](https://github.com/vllm-project/vllm/pull/65508) emit o_proj MXFP8 input from NVFP4 sparse decode kernel
- [#65481](https://github.com/vllm-project/vllm/pull/65481) pick NVFP4 sparse decode splits per XCD
- [#65530](https://github.com/vllm-project/vllm/pull/65530) retune MXFP8 dot_scaled GEMM tiles for M=17-256
- [#63890](https://github.com/vllm-project/vllm/pull/63890) use AITER all-gather for small TP all-gathers
- [#63730](https://github.com/vllm-project/vllm/pull/63730) Kimi-K3 prefill GEMMs on AITER tuned kernels
- [#59124](https://github.com/vllm-project/vllm/pull/59124) opt-in FlyDSL FP8 prefill attention for AITER MLA
- [#63540](https://github.com/vllm-project/vllm/pull/63540) process 4 heads per program in fused_inv_rope_fp8_quant (DSv4)
- [#63888](https://github.com/vllm-project/vllm/pull/63888) skip top-k -1 fill on rows the decode top-k writes (DSv4.1)
- [#63891](https://github.com/vllm-project/vllm/pull/63891) run DSpark fused Markov sampling on gfx950 with --monokernel
- [#65874](https://github.com/vllm-project/vllm/pull/65874) fused GDN MTP supports DSpark K=8 and uses idle SMs at small batch
- [#64510](https://github.com/vllm-project/vllm/pull/64510) enable native small-head kernels in SM90 sparse FlashMLA
- [#61821](https://github.com/vllm-project/vllm/pull/61821) bias in the SM120 NVFP4 CUTLASS GEMM epilogue
- [#65791](https://github.com/vllm-project/vllm/pull/65791) vectorize silu_and_mul_per_block_quant for large inputs
- [#66064](https://github.com/vllm-project/vllm/pull/66064) fuse GDN prefill state gather/scatter with shared Triton kernels
- [#65831](https://github.com/vllm-project/vllm/pull/65831) reduce per-block CPU cost of KV block allocation and caching
- [#65285](https://github.com/vllm-project/vllm/pull/65285) cache parked async KV loads' admission reservations
- [#65773](https://github.com/vllm-project/vllm/pull/65773) cheapen the spin while waiting for model output
- [#64187](https://github.com/vllm-project/vllm/pull/64187) make the EP weight filter EPLB-aware
- [#60882](https://github.com/vllm-project/vllm/pull/60882) incremental scan of required-tool streaming deltas
- [#52875](https://github.com/vllm-project/vllm/pull/52875) render plain completion stream deltas from a template
- [#65867](https://github.com/vllm-project/vllm/pull/65867) write run-batch JSON responses without parsing them back
- [#66227](https://github.com/vllm-project/vllm/pull/66227) warm up DeepGEMM NVFP4 MegaMoE kernels (MiniMax-M3)
- [#65883](https://github.com/vllm-project/vllm/pull/65883) avoid sync when building sparse-attention prefill metadata (MiniMax-M3)
- [#66021](https://github.com/vllm-project/vllm/pull/66021) validate sparse weight patches in one pass (RL)
- [#65589](https://github.com/vllm-project/vllm/pull/65589) don't import vllm.parser from structured_output (startup)
- [#64622](https://github.com/vllm-project/vllm/pull/64622) skip CUDA graph memory profile when estimate is disabled

</details>

<details>
<summary>Kernels & attention (11)</summary>

- [#62725](https://github.com/vllm-project/vllm/pull/62725) gfx942 MLA verify beyond 4 tokens via Triton kernel
- [#65971](https://github.com/vllm-project/vllm/pull/65971) follow-ups to the gfx942 MLA Triton verify kernel
- [#63795](https://github.com/vllm-project/vllm/pull/63795) DSpark sliding-window MLA draft layers
- [#64476](https://github.com/vllm-project/vllm/pull/64476) fuse Markov bias and block combine into Gumbel sampling (DSpark)
- [#65386](https://github.com/vllm-project/vllm/pull/65386) MiniMax m3.1 DSpark drafter monokernel
- [#64994](https://github.com/vllm-project/vllm/pull/64994) up-project MLA decode output before the A2A merge (DCP)
- [#64095](https://github.com/vllm-project/vllm/pull/64095) cross-layer KV cache sharing for MLA
- [#65930](https://github.com/vllm-project/vllm/pull/65930) upgrade FlashInfer to 0.7.3
- [#65743](https://github.com/vllm-project/vllm/pull/65743) remove dead kernels
- [#65627](https://github.com/vllm-project/vllm/pull/65627) keep FA sliding window active under batch invariance
- [#66100](https://github.com/vllm-project/vllm/pull/66100) move CPU ops wrappers to vllm/_cpu_ops.py

</details>

<details>
<summary>MoE & quantization (12)</summary>

- [#62759](https://github.com/vllm-project/vllm/pull/62759) LUT-B MoE with MXFP8 activations: native Rubin kernel plus emulation
- [#46871](https://github.com/vllm-project/vllm/pull/46871) XPU all-to-all EP backend for batched MoE
- [#63349](https://github.com/vllm-project/vllm/pull/63349) deduplicate MoE oracle selection and backend code
- [#51808](https://github.com/vllm-project/vllm/pull/51808) activation quant key override for online MXFP4 linear/MoE
- [#64410](https://github.com/vllm-project/vllm/pull/64410) w4afp8 checkpoints on the W4A8 FP8 MoE path
- [#63711](https://github.com/vllm-project/vllm/pull/63711) Laguna MoE on Zen CPU via grouped W8A16
- [#61897](https://github.com/vllm-project/vllm/pull/61897) routed-experts capture (R3) with pipeline parallelism
- [#64689](https://github.com/vllm-project/vllm/pull/64689) allow a shared routed-expert row restorer
- [#65517](https://github.com/vllm-project/vllm/pull/65517) fix tkw1 rejecting count-free expert metadata, rename AITER QuantMethod
- [#61816](https://github.com/vllm-project/vllm/pull/61816) stop declaring MXFP4 MoE intermediate padding to AITER
- [#57823](https://github.com/vllm-project/vllm/pull/57823) respect padded row strides in top-k routing
- [#65955](https://github.com/vllm-project/vllm/pull/65955) avoid importing humming when resolving quantization configs

</details>

<details>
<summary>Model support (19)</summary>

- [#65745](https://github.com/vllm-project/vllm/pull/65745) add Ricursive Ripple-65B
- [#65826](https://github.com/vllm-project/vllm/pull/65826) add LFM3-Text
- [#65827](https://github.com/vllm-project/vllm/pull/65827) add LFM3-VL
- [#65828](https://github.com/vllm-project/vllm/pull/65828) add LFM3-Audio
- [#61448](https://github.com/vllm-project/vllm/pull/61448) Muse Glimmer fusions for AMD
- [#66334](https://github.com/vllm-project/vllm/pull/66334) Muse Spark Open cleanup
- [#60314](https://github.com/vllm-project/vllm/pull/60314) data-parallel multimodal encoder for Gemma-4
- [#65577](https://github.com/vllm-project/vllm/pull/65577) mm_device_do_normalize for Gemma 4
- [#66393](https://github.com/vllm-project/vllm/pull/66393) migrate Gemma and StableLM to Transformers backend
- [#59767](https://github.com/vllm-project/vllm/pull/59767) migrate Aria to Transformers backend
- [#61813](https://github.com/vllm-project/vllm/pull/61813) use upstream Transformers MiniMaxM3VLConfig
- [#66097](https://github.com/vllm-project/vllm/pull/66097) upstream config for Qwen3-ASR
- [#66388](https://github.com/vllm-project/vllm/pull/66388) upstream config for MOSS-Transcribe-Diarize
- [#65817](https://github.com/vllm-project/vllm/pull/65817) ERNIE-5.5-Flash recipe
- [#65986](https://github.com/vllm-project/vllm/pull/65986) DeepSeek-V4.1-Flash AgentX presets for GB200/B200
- [#66343](https://github.com/vllm-project/vllm/pull/66343) Kimi-K3.1-Pro MI355X concurrency-1 preset
- [#65725](https://github.com/vllm-project/vllm/pull/65725) Kimi-K3.1-Pro TPU serving recipe
- [#66188](https://github.com/vllm-project/vllm/pull/66188) MiniMax-M3.1-Flash MI355X AgentX recipe
- [#65249](https://github.com/vllm-project/vllm/pull/65249) prefix-cache SWA replay on gfx942 (DSv4.1)

</details>

<details>
<summary>Parallelism & scheduling (10)</summary>

- [#65235](https://github.com/vllm-project/vllm/pull/65235) plan_loads and TraceTensor load plan (RL)
- [#49459](https://github.com/vllm-project/vllm/pull/49459) remove per-load completeness checks
- [#65914](https://github.com/vllm-project/vllm/pull/65914) one finish for every model-loader update path
- [#64352](https://github.com/vllm-project/vllm/pull/64352) direct reload resets MoE expert padding at begin
- [#60130](https://github.com/vllm-project/vllm/pull/60130) SimpleCPUOffload: one host buffer per rank, opt-in HugeTLB
- [#57810](https://github.com/vllm-project/vllm/pull/57810) keep offloaded KV tier across pause/sleep
- [#66010](https://github.com/vllm-project/vllm/pull/66010) sleep mode level 2 discards only parameters
- [#61292](https://github.com/vllm-project/vllm/pull/61292) Mooncake async lookup on on_new_request
- [#65160](https://github.com/vllm-project/vllm/pull/65160) MooncakeStore automatic deployment cache prefixes
- [#63231](https://github.com/vllm-project/vllm/pull/63231) default --block-size 16 to 64

</details>

<details>
<summary>Hardware & arch (5)</summary>

- [#63401](https://github.com/vllm-project/vllm/pull/63401) size extensible KV cache from exact VRAM use (ROCm)
- [#62718](https://github.com/vllm-project/vllm/pull/62718) split skinny GEMMs per kernel family to speed ROCm build
- [#62717](https://github.com/vllm-project/vllm/pull/62717) split topk softplus-sqrt instantiations per dtype
- [#63364](https://github.com/vllm-project/vllm/pull/63364) instantiate int4 skinny GEMM per output width
- [#63365](https://github.com/vllm-project/vllm/pull/63365) instantiate fused MUSE-Spark op per head size

</details>

<details>
<summary>API & serving (16)</summary>

- [#65293](https://github.com/vllm-project/vllm/pull/65293) choose chat content format by probing the template (Rust frontend)
- [#65625](https://github.com/vllm-project/vllm/pull/65625) support n > 1 choices (Rust frontend)
- [#65624](https://github.com/vllm-project/vllm/pull/65624) support echo with truncate_prompt_tokens
- [#65853](https://github.com/vllm-project/vllm/pull/65853) namespace tools in the Responses API
- [#65863](https://github.com/vllm-project/vllm/pull/65863) echo prompt-cache and safety_identifier in Responses
- [#65636](https://github.com/vllm-project/vllm/pull/65636) report system_fingerprint from engine config hash
- [#65635](https://github.com/vllm-project/vllm/pull/65635) export vllm:cache_config_info
- [#65622](https://github.com/vllm-project/vllm/pull/65622) count vllm:watermark_requests from the engine flag
- [#64695](https://github.com/vllm-project/vllm/pull/64695) generate through an Llm trait
- [#65294](https://github.com/vllm-project/vllm/pull/65294) keep developer messages in place for templates without the role
- [#65854](https://github.com/vllm-project/vllm/pull/65854) accept an empty tools array
- [#65852](https://github.com/vllm-project/vllm/pull/65852) FastAPI-style JSON 400 errors for dev routes
- [#65623](https://github.com/vllm-project/vllm/pull/65623) pass assistant/tool content parts to HF templates
- [#65621](https://github.com/vllm-project/vllm/pull/65621) accept refusal content parts
- [#65850](https://github.com/vllm-project/vllm/pull/65850) add max_lora label to lora_requests_info
- [#66028](https://github.com/vllm-project/vllm/pull/66028) Kimi K3.1 chat renderer (split 2/5)

</details>

<details>
<summary>Bugfixes (47)</summary>

- [#65158](https://github.com/vllm-project/vllm/pull/65158) docstring style pre-commit hook and single backticks
- [#64528](https://github.com/vllm-project/vllm/pull/64528) bump ruff to 0.17.2 with more lint rules
- [#65554](https://github.com/vllm-project/vllm/pull/65554) fix startup illegal memory access from unaligned extensible KV segments
- [#65463](https://github.com/vllm-project/vllm/pull/65463) re-fit max-model-len auto after extensible KV shrinks
- [#65137](https://github.com/vllm-project/vllm/pull/65137) keep same-host NIXL on NVLink with extensible KV cache
- [#59746](https://github.com/vllm-project/vllm/pull/59746) NIXL: pair P/D blocks by last token across block sizes
- [#65939](https://github.com/vllm-project/vllm/pull/65939) bound Mooncake prefix lookups with a circuit breaker
- [#64298](https://github.com/vllm-project/vllm/pull/64298) fail never-sent P2P offload fetches locally
- [#65124](https://github.com/vllm-project/vllm/pull/65124) abort inbound loads when draining for cache reset
- [#65631](https://github.com/vllm-project/vllm/pull/65631) keep whole-chunk max_load_tokens caps with sliding windows
- [#65237](https://github.com/vllm-project/vllm/pull/65237) keep lazy SimpleCPUOffload stores at GPU eviction end
- [#65640](https://github.com/vllm-project/vllm/pull/65640) refresh streaming request keys after preemption
- [#65593](https://github.com/vllm-project/vllm/pull/65593) make EC connector ZMQ heartbeats effective
- [#64880](https://github.com/vllm-project/vllm/pull/64880) apply DeepSeek-V4 compressor and wo_a LoRA adapters
- [#62517](https://github.com/vllm-project/vllm/pull/62517) DeepSeek V4.1 DSML opener leaking into content
- [#60487](https://github.com/vllm-project/vllm/pull/60487) count attention sinks once in AITER FA chunked extend
- [#65722](https://github.com/vllm-project/vllm/pull/65722) stop AITER FA skipping 1-token prompts
- [#63117](https://github.com/vllm-project/vllm/pull/63117) take AITER MLA KV dtype from group spec
- [#65092](https://github.com/vllm-project/vllm/pull/65092) reserve kpool decode indexer logits during profiling
- [#64886](https://github.com/vllm-project/vllm/pull/64886) refresh derived weight copies after in-place writes (Kimi-K3)
- [#62675](https://github.com/vllm-project/vllm/pull/62675) pad Qwen4Exp PLE n-gram inputs for piecewise graphs
- [#64856](https://github.com/vllm-project/vllm/pull/64856) reserve MSA Q8KV4 prefill workspace (MiniMax-M3.1)
- [#64986](https://github.com/vllm-project/vllm/pull/64986) fix KV-sharing fast prefill hang
- [#65598](https://github.com/vllm-project/vllm/pull/65598) persistent buffer for FlashInfer TRTLLM prefill query offsets
- [#65275](https://github.com/vllm-project/vllm/pull/65275) promised max_query_len for encoder-only FULL graphs
- [#65778](https://github.com/vllm-project/vllm/pull/65778) fix FlashInfer ViT attention for GLM models
- [#65351](https://github.com/vllm-project/vllm/pull/65351) fix Step3-VL encoder output aliasing
- [#65761](https://github.com/vllm-project/vllm/pull/65761) cap encoder-graph frame slots at token budget
- [#66190](https://github.com/vllm-project/vllm/pull/66190) Qwen2.5-Omni video encoder budget from processor limits
- [#66017](https://github.com/vllm-project/vllm/pull/66017) Qwen3-Omni video encoder budget
- [#65412](https://github.com/vllm-project/vllm/pull/65412) Granite4Vision padding tiles
- [#65363](https://github.com/vllm-project/vllm/pull/65363) media cache eviction during reads
- [#64543](https://github.com/vllm-project/vllm/pull/64543) dots_ocr vision QKV split for TP>1
- [#65229](https://github.com/vllm-project/vllm/pull/65229) avoid cancellation in acceptance estimator
- [#65270](https://github.com/vllm-project/vllm/pull/65270) mixed draft-model warmup token budget (MRV2)
- [#65804](https://github.com/vllm-project/vllm/pull/65804) treat standalone draft prefill as decode
- [#66000](https://github.com/vllm-project/vllm/pull/66000) skip VllmConfig re-validation for MTP draft config
- [#65710](https://github.com/vllm-project/vllm/pull/65710) handle EOS in speculative Guidance batches
- [#65539](https://github.com/vllm-project/vllm/pull/65539) PP rank derivation with prefill context parallelism
- [#65792](https://github.com/vllm-project/vllm/pull/65792) hash parallel config before engine init for DP validation
- [#65667](https://github.com/vllm-project/vllm/pull/65667) read routed experts from unkeyed full blocks
- [#63488](https://github.com/vllm-project/vllm/pull/63488) restore engine memory budget after IPC fallback
- [#60047](https://github.com/vllm-project/vllm/pull/60047) register aten::mm out_dtype overloads for batch invariance
- [#60438](https://github.com/vllm-project/vllm/pull/60438) fall back from DeepGEMM when nvcc < 12.9
- [#66016](https://github.com/vllm-project/vllm/pull/66016) never fall back from x.yf CUDA arch to lower minor
- [#63173](https://github.com/vllm-project/vllm/pull/63173) honor token ID logprob overrides on derender paths
- plus 12 more minor bugfixes (frontend, LoRA, pooling, tool parsers, benchmark, Gemma4)

</details>

<details>
<summary>CI & build (14)</summary>

- [#65145](https://github.com/vllm-project/vllm/pull/65145) bake hash-locked KV connectors into CI image and re-enable jobs
- [#62298](https://github.com/vllm-project/vllm/pull/62298) run ROCm-capable tests previously skipped on AMD
- [#65276](https://github.com/vllm-project/vllm/pull/65276) cache a PR's ROCm base image with /ci rocm cache
- [#65957](https://github.com/vllm-project/vllm/pull/65957) cache only ROCm stacks the PR's CI pushed
- [#64131](https://github.com/vllm-project/vllm/pull/64131) keep nightlies off PR-writable images
- [#63574](https://github.com/vllm-project/vllm/pull/63574) raise patched runtime/test dependency floors
- [#66175](https://github.com/vllm-project/vllm/pull/66175) recompile KV connector lock against raised opentelemetry floors
- [#60824](https://github.com/vllm-project/vllm/pull/60824) add zen5 CPU tests
- [#56246](https://github.com/vllm-project/vllm/pull/56246) Rust Frontend CI for Intel GPU
- [#65168](https://github.com/vllm-project/vllm/pull/65168) pluggable shared stores for daemon warmup caches
- [#65652](https://github.com/vllm-project/vllm/pull/65652) replace config compute_hash with compile_factors
- [#65895](https://github.com/vllm-project/vllm/pull/65895) repository-scoped Docker Hub secret for release publishing
- [#66313](https://github.com/vllm-project/vllm/pull/66313) bump tensorizer to 2.12.1
- plus 6 more minor CI updates (sharding, labels, test consolidation)

</details>

<details>
<summary>Tests (4)</summary>

- [#61796](https://github.com/vllm-project/vllm/pull/61796) UMBP standalone runtime coverage
- [#62529](https://github.com/vllm-project/vllm/pull/62529) TP2 PCP2 canonical mapping coverage
- [#66206](https://github.com/vllm-project/vllm/pull/66206) cover MXFP4 W4A16 intermediate pad reaching AITER
- [#56508](https://github.com/vllm-project/vllm/pull/56508) no-NIXL import test for EC connector

</details>

<details>
<summary>Other (6)</summary>

- #65651 not shown in provided data; omitted
- [#42837](https://github.com/vllm-project/vllm/pull/42837) shuffle safetensor weight files
- [#66066](https://github.com/vllm-project/vllm/pull/66066) not applicable; omitted
- [#65834](https://github.com/vllm-project/vllm/pull/65834) fix missing MLA verify parameter types in API docs
- [#65851](https://github.com/vllm-project/vllm/pull/65851) keep whitespace in HY tool-call argument names (Rust frontend)
- [#66111](https://github.com/vllm-project/vllm/pull/66111) reuse HF reference across use_prompt_embeds in CI

</details>

---
_Generated by inferadar-summarize from the committed changelog JSON (vllm.json), the deterministic source of truth. This file mentions no users and notifies no PRs._
<!-- inferadar-source-sha256: ac7854b397998c57e9933c555575015dee14aec0e68ddd866a2804dd29594b60 -->
