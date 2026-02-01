# M/M/1 Queue Calculator (Streamlit)

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## What it does
- Takes arrival rate (λ per hour) and average service time (minutes per customer)
- Computes M/M/1 performance measures: ρ, P0, Ls, Lq, Ws, Wq
- Computes state probability P(N=n) and shows a table of P(N=n) for n=0..Nmax
