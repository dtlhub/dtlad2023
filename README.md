# dtlad2023

[![check-services](https://github.com/dtlhub/dtlad2023/actions/workflows/check-services.yml/badge.svg?branch=master&event=push)](https://github.com/dtlhub/dtlad2023/actions/workflows/check-services.yml)

![Scoreboard leaders](/screenshots/top.png)

## Services

| Service                                        | Language            | Vulns                                                                     | Authors                                 |
| ---------------------------------------------- | ------------------- | ------------------------------------------------------------------------- | --------------------------------------- |
| [amogus_plus_plus](services/amogus_plus_plus/) | JavaScript & Svelte | Default creds, missconfiguration, path traversal, prototype pollution     | [@LeKSuS](https://t.me/tarasovion)      |
| [jeopardy](services/jeopardy/)                 | Python              | Default keys, using stream cipher for signing, small nonces for ecdsa     | [@defkit](https://t.me/defkit)          |
| [msngr](services/msngr/)                       | Python              | Linear sbox in substitution-permutation cipher, dlp with chosen parameters| [@defkit](https://t.me/defkit)          |
| [schizichs](services/schizichs/)               | Go                  | Default JWT key, Vulnerable math in error function, full lab info leak    | [@synerr](https://t.me/eat_people)      |
| [Zapiski](services/Zapiski/)                   | C                   | Ujazvimost'                                                               | [@c3N1T3Lb](https://t.me/c3N1T3Lb)      |

## Infrastructure

- DevOps: [@LeKSuS](https://t.me/tarasovion)
- Checksystem: [ForcAD](https://github.com/pomo-mondreganto/ForcAD)

## Writeups & sploits

- [amogus_plus_plus](/sploits/amogus_plus_plus/)
- [jeopardy](/sploits/jeopardy/)
- [schizichs](/sploits/schizichs/)
- [msngr](/sploits/msngr)
- [Zapiski](sploits/Zapiski/)   
