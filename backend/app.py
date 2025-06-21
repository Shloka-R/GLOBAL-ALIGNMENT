
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def needleman_wunsch(seq1, seq2, match, mismatch, gap):
    m, n = len(seq1), len(seq2)
    score = [[0]*(n+1) for _ in range(m+1)]
    for i in range(m+1):
        score[i][0] = i * gap
    for j in range(n+1):
        score[0][j] = j * gap

    for i in range(1, m+1):
        for j in range(1, n+1):
            if seq1[i-1] == seq2[j-1]:
                diag = score[i-1][j-1] + match
            else:
                diag = score[i-1][j-1] + mismatch
            score[i][j] = max(diag, score[i-1][j] + gap, score[i][j-1] + gap)

    aligned1, aligned2 = "", ""
    i, j = m, n
    while i > 0 and j > 0:
        current = score[i][j]
        if seq1[i-1] == seq2[j-1]:
            diag = score[i-1][j-1] + match
        else:
            diag = score[i-1][j-1] + mismatch
        if current == diag:
            aligned1 = seq1[i-1] + aligned1
            aligned2 = seq2[j-1] + aligned2
            i -= 1
            j -= 1
        elif current == score[i-1][j] + gap:
            aligned1 = seq1[i-1] + aligned1
            aligned2 = "-" + aligned2
            i -= 1
        else:
            aligned1 = "-" + aligned1
            aligned2 = seq2[j-1] + aligned2
            j -= 1

    while i > 0:
        aligned1 = seq1[i-1] + aligned1
        aligned2 = "-" + aligned2
        i -= 1
    while j > 0:
        aligned1 = "-" + aligned1
        aligned2 = seq2[j-1] + aligned2
        j -= 1

    similarity = sum([1 for a, b in zip(aligned1, aligned2) if a == b])
    percentage = round((similarity / len(aligned1)) * 100, 2)
    
    return aligned1, aligned2, percentage

@app.route('/align', methods=['POST'])
def align_sequences():
    data = request.json
    seq1 = data['seq1'].upper()
    seq2 = data['seq2'].upper()
    match = int(data['match'])
    mismatch = int(data['mismatch'])
    gap = int(data['gap'])

    aligned1, aligned2, similarity = needleman_wunsch(seq1, seq2, match, mismatch, gap)
    return jsonify({
        "aligned_seq1": aligned1,
        "aligned_seq2": aligned2,
        "similarity": f"{similarity}%"
    })

if __name__ == '__main__':
    app.run(debug=True)
