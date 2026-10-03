# Third-Party Data Attribution

## OpenJLPT

Kansu uses data from **OpenJLPT**, a derived Japanese language-learning
dataset.

Source:
https://github.com/evanclan/OpenJLPT

License:
**Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)**

License URL:
https://creativecommons.org/licenses/by-sa/4.0/

The OpenJLPT data used by Kansu has been imported into the project's
local SQLite database.

Changes made to the data include transforming the source data into
Kansu's database schema and associating vocabulary entries with kanji.

### Upstream Sources

OpenJLPT incorporates data from the following sources:

| Source | Used for | License | Link |
|---|---|---|---|
| **Jonathan Waller's JLPT Resources** | JLPT level assignments for vocabulary and kanji, and English vocabulary glosses | CC BY | https://www.tanos.co.uk/jlpt/ |
| **JMdict** — EDRDG | Vocabulary IDs, parts of speech, readings, spellings, and glosses | CC BY-SA 4.0 | https://www.edrdg.org/jmdict/j_jmdict.html |
| **KANJIDIC2** — EDRDG | Kanji readings, meanings, stroke counts, grade, frequency, radical, and name readings | CC BY-SA 4.0 | https://www.edrdg.org/wiki/KANJIDIC_Project.html |
| **Tatoeba** | Japanese-English example sentences | CC BY 2.0 FR | https://tatoeba.org |

For the complete data-source and attribution information, see the
OpenJLPT `NOTICE.md`:
https://github.com/evanclan/OpenJLPT/blob/main/NOTICE.md

### License of Derived Data

The OpenJLPT-derived data included in Kansu remains subject to
**CC BY-SA 4.0**.

Any redistribution of the OpenJLPT-derived dataset or further
derivatives must comply with the CC BY-SA 4.0 license, including its
ShareAlike and attribution requirements.

The MIT License for Kansu's source code does not apply to
OpenJLPT-derived data.

OpenJLPT and its upstream projects are not affiliated with or endorsed
by Kansu.