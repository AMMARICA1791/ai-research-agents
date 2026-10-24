# Public Project Islands — Developer Directory

This is the public entry point for projects produced by the [AI Research Agents radar](https://github.com/AMMARICA1791/ai-research-agents). **Each linked repository is public.** Projects are experimental prototypes, not validated products. Developers are welcome to open issues and contribute tested fixes.

## Browse by purpose

| Area | What to explore | Public repositories |
| --- | --- | --- |
| Authorization & agent security | Experimental authorization-gate prototypes; compare failure cases and suggest regression tests | [Main security prototype](https://github.com/AMMARICA1791/radar-agent-security), [experiment A](https://github.com/AMMARICA1791/radar-agent-security-22e575a0c5d60e6f), [experiment B](https://github.com/AMMARICA1791/radar-agent-security-4739348ea32ca8ae), [experiment C](https://github.com/AMMARICA1791/radar-agent-security-4ff780399017c08e), [experiment D](https://github.com/AMMARICA1791/radar-agent-security-83ab5580b21e5403), [experiment E](https://github.com/AMMARICA1791/radar-agent-security-eb73a5e6221f7ebc) |
| Source claim traceability | Experiments connecting claims to sources and testable evidence | [Experiment A](https://github.com/AMMARICA1791/radar-source-claim-177b2d16f2e167f3), [experiment B](https://github.com/AMMARICA1791/radar-source-claim-1980fd2a6a586eda) |
| Privacy | Experimental privacy checks | [Privacy prototype](https://github.com/AMMARICA1791/radar-privacy) |
| Evidence provenance | Experimental source/evidence provenance | [Provenance prototype](https://github.com/AMMARICA1791/radar-provenance) |

The hexadecimal suffixes above are legacy signal identifiers, **not human-readable project titles**. They are kept in this index only to preserve working links to already published repositories.

## Naming policy for new islands

New public repositories use human-readable functional names such as `radar-authorization-trust-gate` and `radar-source-claim-traceability`. Signal IDs remain internal metadata. Experiments sharing a project family should be curated together instead of published as an unbounded stream of hash-suffixed repos. A common category does **not** prove identical functionality; preserve distinct evidence and tests before consolidating.

## How to contribute

1. Choose an area and read a project's README, hypothesis and tests.
2. Reproduce the behavior with `python -m unittest discover -s . -p 'test_*.py' -v`.
3. Open an issue in that project's repository with the exact reproduction steps and expected/actual results.
4. Submit a pull request containing the smallest possible fix and a regression test.

Do not share secrets or personal data. Generated hypotheses are unverified until independently reproduced. No existing repository will be deleted or overwritten as part of the naming transition.
