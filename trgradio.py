import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import gradio as gr
import os
from stocksymbol import StockSymbol
import riskfolio as rp

api_key = '085fa333-acf8-4328-9828-e6afb07c23d9 '
ss = StockSymbol(api_key)

assets_portfolio = []

def combine_assets(asset):
    assets_portfolio.append(asset)
    return(assets_portfolio)

def validate_date(date1, date2):    
    if date2 - date1 > 0:
        output = "You select a period from " + str(date1) + " to " + str(date2)
    else:
        output = "Incorrect period, first date need to be inferior to second date"
    return(output)

def prediction(date1, date2, assets_portfolio):

    return 


def best_portfolio(date1, date2, assets_portfolio):
    # pour le momemt c'est juste moyenne risque gain 
    data = yf.download(assets_portfolio, start =date1, end =date2)
    data = data.loc[:,('Adj Close', slice(None))]
    data.columns = assets_portfolio
    assets = data.pct_change().dropna()
    Y = assets
    port = rp.Portfolio(returns=Y)
    pd.options.display.float_format = '{:.4%}'.format
    rm = 'MSV' 
    port.assets_stats(method_mu='hist', method_cov='hist', d=0.94)
    w1 = port.optimization(model='Classic', rm=rm, obj='Sharpe', rf=0.0, l=0, hist=True)
    ws = port.efficient_frontier(model='Classic', rm=rm, points=20, rf=0, hist=True)
    w2 = port.rp_optimization(model='Classic', rm=rm, rf=0, b=None, hist=True)
    label = 'Max Risk Adjusted Return Portfolio'
    rp.plot_frontier(w_frontier=ws, mu=port.mu, cov=port.cov, returns=port.returns,
                       rm=rm, rf=0, alpha=0.05, cmap='viridis', w=w1,
                       label=label, marker='*', s=16, c='r',
                       height=6, width=10, t_factor=252, ax=None)
    rp.plot_pie(w=w1, title='Portfolio', height=6, width=10,
                 cmap="tab20", ax=None)
    return

symbol_only_list_us = ss.get_symbol_list(market="us", symbols_only=True)
list_assets = list(symbol_only_list_us)
list_assets.sort()

with gr.Blocks() as demo:
    
    with gr.Column():
        
        choose_asset = gr.inputs.Dropdown(list_assets, label="Choose an asset to add")
        btn_asset = gr.Button(value="Add to portfolio")
        asset_selected = gr.Textbox(value="", label="Assets selected")
        btn_asset.click(combine_assets, inputs=[choose_asset], outputs=[asset_selected])
    
    with gr.Column():

        date1 = gr.inputs.Slider(1900,2021,label="First date") 
        date2 = gr.inputs.Slider(1900,2021,label="Second date")
        btn_date = gr.Button(value="Validate date")
        period_selected = gr.Textbox(value="", label="Selected period")
        btn_date.click(validate_date, inputs=[date1, date2], outputs=[period_selected])
    
    with gr.Row():
        
        btn_predict = gr.Button(value="Run prediction")
        # TO DEFINE =
        # btn_predict.click(prediction, inputs=[date1, date2, asset_selected], outputs=[ TO DEFINE ]])
    
        btn_bestportfolio = gr.Button(value="Run best portfolio") #change the name for this button ?
        # TO DEFINE =
        # btn_bestportfolio.click(best_portfolio, inputs=[date1, date2, asset_selected], outputs=[ TO DEFINE ]]))


if __name__ == "__main__":
    demo.launch()
