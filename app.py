import streamlit as st
from scipy.stats import hypergeom
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np



#Methods
def ConvertToPercentage(num):
    return round(num * 100,2)

def BuildProbabilityStr(msg,k,num):
    return f'{msg} {k}: {ConvertToPercentage(num)} %'

def CalculateAndWriteProbability(k,M,n,N,hpd):

    #Exact k
    pExact = hpd.pmf(k)
    pExactStr = BuildProbabilityStr('Draw exact',k,pExact)
    st.write(pExactStr)

    #Less  k
    pLess = hypergeom.cdf(k-1, M, n, N)
    pLessStr = BuildProbabilityStr('Draw less than',k,pLess)
    st.write(pLessStr)

    #Less or equal k
    pLessEqual = hypergeom.cdf(k, M, n, N)
    pLessEqualStr = BuildProbabilityStr('Draw less than or equal than',k,pLessEqual)
    st.write(pLessEqualStr)

    #More k
    pMore = 1 - pLessEqual
    pMoreStr = BuildProbabilityStr('Draw more than',k,pMore)
    st.write(pMoreStr)

    #More or equal k
    pMoreEqual = 1 - pLess
    pMoreEqualStr = BuildProbabilityStr('Draw more or equal than',k, pMoreEqual)
    st.write(pMoreEqualStr)

def PlotDistribution(n,hpd):
    st.write('## Probability Distribution')
    x = np.arange(0, n+1)
    pmf_cards = hpd.pmf(x)
    plt.style.use('dark_background')
    #plt.style.use('ggplot')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.plot(x, pmf_cards, 'bo')
    ax.vlines(x, 0, pmf_cards, lw=2)
    ax.set_xlabel('# of (copies/equal considered) cards')
    ax.set_ylabel('hypergeom PMF')
    #plotting the figure
    st.pyplot(fig)
    

#Main prog
st.title("Yu-Gi-Oh! Probability Calculator")

#Reading unsigned integer values
#TODO: Check values
decksize = st.number_input('Enter your decksize: ',min_value = 0,value = 40,format="%u")
amountSuccess = st.number_input('Enter the amount of draw succeses: ',min_value = 0,value = 1,format="%u")
amountCopies = st.number_input('Enter the of copies you have in your deck : ',min_value = 0,value = 3,format="%u")
amountCardsAtTurnBegin = st.number_input('Enter the amount of cards you draw on your first turn: ',min_value = 0,value = 5,format="%u")
M = decksize
n = amountCopies
N = amountCardsAtTurnBegin
k = amountSuccess

#Performing calculations
hpd = hypergeom(M, n, N)

CalculateAndWriteProbability(k,M,n,N,hpd)

PlotDistribution(n,hpd)

#Info
st.write('#### Yu-Gi-Oh! is a trademark of Shueisha and Konami. This project is not affiliated with or endorsed by Shueisha or Konami.')