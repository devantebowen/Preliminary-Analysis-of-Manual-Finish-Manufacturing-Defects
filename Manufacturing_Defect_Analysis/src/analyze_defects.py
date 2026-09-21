"""Reproduce descriptive summaries; no external dependencies or causal claims."""
from collections import Counter
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def summary(rows, field):
    counts = Counter(row[field] for row in rows)
    total = len(rows)
    running = 0
    output = []
    for category, count in sorted(counts.items(), key=lambda pair: (-pair[1], pair[0])):
        running += count
        output.append([category, count, round(count / total * 100, 4),
                       round(running / total * 100, 4)])
    return output


def write_summary(filename, field, values):
    with (ROOT / 'results' / filename).open('w', newline='', encoding='utf-8') as stream:
        writer = csv.writer(stream)
        writer.writerow([field, 'defect_count', 'percent_of_records', 'cumulative_percent'])
        writer.writerows(values)


def main():
    with (ROOT / 'data' / 'manufacturing_defects.csv').open(newline='', encoding='utf-8-sig') as stream:
        reader = csv.DictReader(stream)
        required = {'Production Model', 'Defect Type', 'Defect Observation Area', 'Inspection Week'}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f'Missing required columns: {sorted(missing)}')
        rows = list(reader)
    if not rows:
        raise ValueError('The dataset contains no records.')
    (ROOT / 'results').mkdir(exist_ok=True)
    models = summary(rows, 'Production Model')
    write_summary('defects_by_model.csv', 'Production Model', models)
    write_summary('defects_by_type.csv', 'Defect Type', summary(rows, 'Defect Type'))
    write_summary('defects_by_observation_area.csv', 'Defect Observation Area',
                  summary(rows, 'Defect Observation Area'))
    top_models = [row[0] for row in models[:3]]
    for model in top_models:
        subset = [row for row in rows if row['Production Model'] == model]
        name = model.lower().replace(' ', '_').replace('-', '_')
        write_summary(f'{name}_defects.csv', 'Defect Type', summary(subset, 'Defect Type'))
    weeks = sorted({row['Inspection Week'] for row in rows})
    print(f'Records: {len(rows):,}; inspection weeks: {weeks[0]} to {weeks[-1]} ({len(weeks)} distinct)')
    for model, count, share, _ in models[:3]:
        print(f'{model}: {count} defects ({share:.1f}%)')
    top_count = sum(row[1] for row in models[:3])
    print(f'Top three combined: {top_count:,} ({top_count / len(rows):.1%})')
    bridges = [row for row in rows if row['Defect Type'] == 'solder bridge']
    selected = {'Model 595214-125', 'Model 595242-854'}
    selected_bridges = sum(row['Production Model'] in selected for row in bridges)
    if bridges:
        print(f'Solder bridges in models 595214-125 and 595242-854: '
              f'{selected_bridges}/{len(bridges)} ({selected_bridges / len(bridges):.1%})')
    print('Summary CSVs written to results/. Counts represent observations, not defect rates.')


if __name__ == '__main__':
    main()
