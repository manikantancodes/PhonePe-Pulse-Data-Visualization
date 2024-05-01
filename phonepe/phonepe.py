import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import json
from PIL import Image

mydb =psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe_data",
                        password="mani94")
cursor = mydb.cursor()

#Dataframe
#sql connection
#aggregated_insurance_datafrane

cursor.execute("SELECT * FROM aggregated_insurance")
aggregated_insurance_data = cursor.fetchall()

aggregated_insurance_df = pd.DataFrame(aggregated_insurance_data, columns=
                                      ("States", "Years","Quarter", "Transaction_type", 
                                        "Transaction_count", "Transaction_amount"))


#Aggregated_transaction_datframe
cursor.execute("SELECT * FROM aggregated_transaction")
aggregated_transaction_data = cursor.fetchall()

aggregated_transaction_df = pd.DataFrame(aggregated_transaction_data, columns=
                                         ("States", "Years", "Quarter", "Transaction_type",
                                          "Transaction_count", "Transaction_amount"))

#Aggregated_user_dataframe
cursor.execute("SELECT * FROM aggregated_user")
aggregated_user_data = cursor.fetchall()

aggregated_user_df = pd.DataFrame(aggregated_user_data, columns=
                                   ("States", "Years", "Quarter", "Brands",
                                    "Transaction_count", "Percentage"))

#Map_insurance_dataframe
cursor.execute("SELECT * FROM map_insurance")
map_insurance_data = cursor.fetchall()

map_insurance_df = pd.DataFrame(map_insurance_data, columns=
                                ("States", "Years", "Quarter", "Districts",
                                 "Transaction_count", "Transaction_amount"))

#Map_transaction_dataframe
cursor.execute("SELECT * FROM map_transaction")
map_transaction_data = cursor.fetchall()

map_transaction_df = pd.DataFrame(map_transaction_data, columns=
                                  ("States", "Years", "Quarter", "District",
                                   "Transaction_count", "Transaction_amount"))

#Map_user_dataframe
cursor.execute("SELECT * FROM map_user")
map_user_data = cursor.fetchall()

map_user_df = pd.DataFrame(map_user_data, columns=
                            ("States", "Years", "Quarter", "District",
                             "RegisteredUsers", "AppOpens"))

#Top_insurance_dataframe
cursor.execute("SELECT * FROM top_insurance")
top_insurance_data = cursor.fetchall()

top_insurance_df = pd.DataFrame(top_insurance_data, columns=
                                ("States", "Years", "Quarter", "Pincodes",
                                 "Transaction_count", "Transaction_amount"))

#Top_transaction_dataframe
cursor.execute("SELECT * FROM top_transaction")
top_transaction_data = cursor.fetchall()

top_transaction_df = pd.DataFrame(top_transaction_data, columns=
                                  ("States", "Years", "Quarter", "Pincodes",
                                   "Transaction_count", "Transaction_amount"))
#Top_user_dataframe
cursor.execute("SELECT * FROM top_user")
top_user_data = cursor.fetchall()

top_user_df = pd.DataFrame(top_user_data, columns=
                           ("States", "Years", "Quarter", "Pincodes",
                            "RegisteredUsers"))




def Transaction_Amount_Count_Year(df, year):
    transaction_yac = df[df["Years"] == year]
    transaction_yac.reset_index(drop=True, inplace=True)

    transaction_yacg = transaction_yac.groupby("States")[["Transaction_amount", "Transaction_count"]].sum()
    transaction_yacg.reset_index(inplace=True)

    # Define 'data1' outside the function to avoid reloading it every time the function is called
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)

    


    st.write(f"### {year} TRANSACTION AMOUNT")
    fig_amount = px.bar(transaction_yac, x="States", y="Transaction_amount",
                        color_discrete_sequence=px.colors.sequential.Blues_r, height=600, width=600)
    st.plotly_chart(fig_amount)

    st.write(f"### {year} TRANSACTION AMOUNT MAP")
    fig_indiamap_1 = px.choropleth(transaction_yacg, geojson=data1, locations="States",
                                    featureidkey="properties.ST_NM",
                                    color="Transaction_amount", color_continuous_scale="Rainbow",
                                    range_color=(transaction_yacg["Transaction_amount"].min(),
                                                    transaction_yacg["Transaction_amount"].max()),
                                    hover_name="States", title=f"{year} TRANSACTION AMOUNT", fitbounds="locations",
                                    height=600, width=600)
    fig_indiamap_1.update_geos(visible=False)
    st.plotly_chart(fig_indiamap_1)


    st.write(f"### {year} TRANSACTION COUNT")
    fig_count = px.bar(transaction_yac, x="States", y="Transaction_count",
                        color_discrete_sequence=px.colors.sequential.Blackbody, height=600, width=400)
    st.plotly_chart(fig_count)

    st.write(f"### {year} TRANSACTION COUNT MAP")
    fig_indiamap_2 = px.choropleth(transaction_yacg, geojson=data1, locations="States",
                                    featureidkey="properties.ST_NM",
                                    color="Transaction_count", color_continuous_scale="Rainbow",
                                    range_color=(transaction_yacg["Transaction_count"].min(),
                                                    transaction_yacg["Transaction_count"].max()),
                                    hover_name="States", title=f"{year} TRANSACTION COUNT", fitbounds="locations",
                                    height=600, width=600)
    fig_indiamap_2.update_geos(visible=False)
    st.plotly_chart(fig_indiamap_2)

    return transaction_yac




def Transaction_Amount_Count_Year_Quarter(df,quarter):
    transaction_yacq=df[df["Quarter"] == quarter ]
    transaction_yacq.reset_index(drop = True,inplace=True)


    transaction_yacqg= transaction_yacq.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    transaction_yacqg.reset_index(inplace=True)
    st.dataframe(transaction_yacq)

    col1, col2 =st.columns(2)
 
    with col1:
            fig_q_count=px.bar(transaction_yacq, x="States", y="Transaction_count",title=f"{transaction_yacq['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                                                color_discrete_sequence=px.colors.sequential.Blackbody)
            st.plotly_chart(fig_q_count)

    with col2:

            fig_q_amount=px.bar(transaction_yacq, x="States", y="Transaction_amount",title=f"{transaction_yacq['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                                                color_discrete_sequence=px.colors.sequential.Blues_r)
            st.plotly_chart(fig_q_amount)


    col1, col2 =st.columns(2)
 
    with col1:
            url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            response = requests.get(url)
            data1 = json.loads(response.content)
            
            figure_indiamap_1 = px.choropleth(transaction_yacqg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                        color="Transaction_amount", color_continuous_scale="Rainbow",
                                        range_color=(transaction_yacqg["Transaction_amount"].min(), transaction_yacqg["Transaction_amount"].max()),
                                        hover_name="States", title=f"{transaction_yacq['Years'].min()}YEAR{quarter} QUARTER TRANSACTION AMOUNT", fitbounds="locations",
                                        height=600, width=600)
            figure_indiamap_1.update_geos(visible=False)
            st.plotly_chart(figure_indiamap_1)

    with col2:
            figure_indiamap_2 = px.choropleth(transaction_yacqg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                        color="Transaction_count", color_continuous_scale="Rainbow",
                                        range_color=(transaction_yacqg["Transaction_count"].min(), transaction_yacqg["Transaction_count"].max()),
                                        hover_name="States", title=f"{transaction_yacq['Years'].min()}YEAR{quarter} QUARTER TRANSACTION COUNT", fitbounds="locations",
                                        height=600, width=600)
            figure_indiamap_2.update_geos(visible=False)
            st.plotly_chart(figure_indiamap_2)

    return transaction_yacq

   
def Aggre_Trans_Transaction_type(df, state):
        df_state= df[df["States"] == state ]
        df_state.reset_index(drop= True, inplace= True)

        df_stateg= df_state.groupby("Transaction_type")[["Transaction_count", "Transaction_amount"]].sum()
        df_stateg.reset_index(inplace= True)

        col1,col2= st.columns(2)
        with col1:

            fig_pie_1= px.pie(data_frame=df_stateg, values= "Transaction_amount", names= "Transaction_type", width= 600,
                            title= f"{state.upper()} TRANSACTION TYPES AND TRANSACTION AMOUNT", hole= 0.5)
            st.plotly_chart(fig_pie_1)

        with col2:

            fig_pie_2= px.pie(data_frame=df_stateg, values= "Transaction_count", names= "Transaction_type", width= 600,
                            title= f"{state.upper()} TRANSACTION TYPES AND TRANSACTION AMOUNT", hole= 0.5)
            st.plotly_chart(fig_pie_2)


def Aggre_user_plot_1(df,year):
    agg_user_year= df[df["Years"] == year]
    agg_user_year.reset_index(drop= True, inplace= True)
    
    agg_user_yearg= pd.DataFrame(agg_user_year.groupby("Brands")["Transaction_count"].sum())
    agg_user_yearg.reset_index(inplace= True)

    fig_line_1= px.bar(agg_user_yearg, x="Brands",y= "Transaction_count", title=f"{year} BRANDS AND TRANSACTION COUNT",
                    width=1000,color_discrete_sequence=px.colors.sequential.haline_r)
    st.plotly_chart(fig_line_1)

    return agg_user_year

def Aggre_user_plot_2(df,quarter):
    agg_user_quarter= df[df["Quarter"] == quarter]
    agg_user_quarter.reset_index(drop= True, inplace= True)

    fig_pie_1= px.pie(data_frame=agg_user_quarter, names= "Brands", values="Transaction_count", hover_data= "Percentage",
                      width=1000,title=f"{quarter} QUARTER TRANSACTION COUNT PERCENTAGE",hole=0.5, color_discrete_sequence= px.colors.sequential.Magenta_r)
    st.plotly_chart(fig_pie_1)

    return agg_user_quarter

def Aggre_user_plot_3(df,state):
    agg_user_states= df[df["States"] == state]
    agg_user_states.reset_index(drop= True, inplace= True)

    agg_user_statesg= pd.DataFrame(agg_user_states.groupby("Brands")["Transaction_count"].sum())
    agg_user_statesg.reset_index(inplace= True)

    fig_scatter_1= px.line(agg_user_statesg, x= "Brands", y= "Transaction_count", markers= True,width=1000)
    st.plotly_chart(fig_scatter_1)

def map_insure_plot_1(df,state):
    map_insurance_year= df[df["States"] == state]
    map_insurance_yearg= map_insurance_year.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    map_insurance_yearg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_bar_1= px.bar(map_insurance_yearg, x= "Districts", y= "Transaction_amount",
                              width=600, height=500, title= f"{state.upper()} DISTRICTS TRANSACTION AMOUNT",
                              color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_map_bar_1)

    with col2:
        fig_map_bar_1= px.bar(map_insurance_yearg, x= "Districts", y= "Transaction_count",
                              width=600, height= 500, title= f"{state.upper()} DISTRICTS TRANSACTION COUNT",
                              color_discrete_sequence= px.colors.sequential.Mint)
        
        st.plotly_chart(fig_map_bar_1)

def map_insure_plot_2(df,state):
    map_insurance_year= df[df["States"] == state]
    map_insurance_yearg= map_insurance_year.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    map_insurance_yearg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_pie_1= px.pie(map_insurance_yearg, names= "Districts", values= "Transaction_amount",
                              width=600, height=500, title= f"{state.upper()} DISTRICTS TRANSACTION AMOUNT",
                              hole=0.5,color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_map_pie_1)

    with col2:
        fig_map_pie_1= px.pie(map_insurance_yearg, names= "Districts", values= "Transaction_count",
                              width=600, height= 500, title= f"{state.upper()} DISTRICTS TRANSACTION COUNT",
                              hole=0.5,  color_discrete_sequence= px.colors.sequential.Oranges_r)
        
        st.plotly_chart(fig_map_pie_1)

def map_user_plot_1(df, year):
    map_user_y= df[df["Years"] == year]
    map_user_y.reset_index(drop= True, inplace= True)
    map_user_yg= map_user_y.groupby("States")[["RegisteredUser", "AppOpens"]].sum()
    map_user_yg.reset_index(inplace= True)

    fig_map_user_plot_1= px.line(map_user_yg, x= "States", y= ["RegisteredUser","AppOpens"], markers= True,
                                width=1000,height=800,title= f"{year} REGISTERED USER AND APPOPENS", color_discrete_sequence= px.colors.sequential.Viridis_r)
    st.plotly_chart(fig_map_user_plot_1)

    return map_user_y

def map_user_plot_2(df, quarter):
    map_user_yq= df[df["Quarter"] == quarter]
    map_user_yq.reset_index(drop= True, inplace= True)
    map_user_yqg= map_user_yq.groupby("States")[["RegisteredUser", "AppOpens"]].sum()
    map_user_yqg.reset_index(inplace= True)

    fig_map_user_plot_1= px.line(map_user_yqg, x= "States", y= ["RegisteredUser","AppOpens"], markers= True,
                                title= f"{df['Years'].min()}, {quarter} QUARTER REGISTERED USER AND APPOPENS",
                                width= 1000,height=800,color_discrete_sequence= px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_map_user_plot_1)

    return map_user_yq

def map_user_plot_3(df, state):
    map_user_yqs= df[df["States"] == state]
    map_user_yqs.reset_index(drop= True, inplace= True)
    map_user_yqsg= map_user_yqs.groupby("Districts")[["RegisteredUser", "AppOpens"]].sum()
    map_user_yqsg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_user_plot_1= px.bar(map_user_yqsg, x= "RegisteredUser",y= "Districts",orientation="h",
                                    title= f"{state.upper()} REGISTERED USER",height=800,
                                    color_discrete_sequence= px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_plot_1)

    with col2:
        fig_map_user_plot_2= px.bar(map_user_yqsg, x= "AppOpens", y= "Districts",orientation="h",
                                    title= f"{state.upper()} APPOPENS",height=800,
                                    color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_map_user_plot_2)

def top_user_plot_1(df,year):
    top_user_y= df[df["Years"] == year]
    top_user_y.reset_index(drop= True, inplace= True)

    top_user_yg= pd.DataFrame(top_user_y.groupby(["States","Quarter"])["RegisteredUser"].sum())
    top_user_yg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(top_user_yg, x= "States", y= "RegisteredUser", barmode= "group", color= "Quarter",
                            width=1000, height= 800, color_continuous_scale= px.colors.sequential.Burgyl)
    st.plotly_chart(fig_top_plot_1)

    return top_user_y

def top_user_plot_2(df,state):
    top_user_ys= df[df["States"] == state]
    top_user_ys.reset_index(drop= True, inplace= True)

    top_user_ysg= pd.DataFrame(top_user_ys.groupby("Quarter")["RegisteredUser"].sum())
    top_user_ysg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(top_user_ys, x= "Quarter", y= "RegisteredUser",barmode= "group",
                           width=1000, height= 800,color= "RegisteredUser",hover_data="Pincodes",
                            color_continuous_scale= px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_plot_1)

def ques1():
    brand= aggregated_user_df[["Brands","Transaction_count"]]
    brand1= brand.groupby("Brands")["Transaction_count"].sum().sort_values(ascending=False)
    brand2= pd.DataFrame(brand1).reset_index()

    fig_brands= px.pie(brand2, values= "Transaction_count", names= "Brands", color_discrete_sequence=px.colors.sequential.dense_r,
                       title= "Top Mobile Brands of Transaction_count")
    return st.plotly_chart(fig_brands)

def ques2():
    Low_trans= aggregated_transaction_df[["States", "Transaction_amount"]]
    Low_trans1= Low_trans.groupby("States")["Transaction_amount"].sum().sort_values(ascending= True)
    Low_trans2= pd.DataFrame(Low_trans1).reset_index().head(10)

    fig_Low_transs= px.bar(Low_trans2, x= "States", y= "Transaction_amount",title= "LOWEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_Low_transs)

def ques3():
    Top_high_transaction= map_transaction_df[["Districts", "Transaction_amount"]]
    Top_high_transaction1= Top_high_transaction.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=False)
    Top_high_transaction2= pd.DataFrame(Top_high_transaction1).head(10).reset_index()

    fig_Top_high_transaction= px.pie(Top_high_transaction2, values= "Transaction_amount", names= "Districts", title="TOP 10 DISTRICTS OF HIGHEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Emrld_r)
    return st.plotly_chart(fig_Top_high_transaction)

def ques4():
    Top_high_transaction= map_transaction_df[["Districts", "Transaction_amount"]]
    Top_high_transaction1= Top_high_transaction.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=True)
    Top_high_transaction2= pd.DataFrame(Top_high_transaction1).head(10).reset_index()

    fig_Top_high_transaction= px.pie(Top_high_transaction2, values= "Transaction_amount", names= "Districts", title="TOP 10 DISTRICTS OF LOWEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Greens_r)
    return st.plotly_chart(fig_Top_high_transaction)


def ques5():
    sa= map_user_df[["States", "AppOpens"]]
    sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=False)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "States", y= "AppOpens", title="Top 10 States With AppOpens",
                color_discrete_sequence= px.colors.sequential.deep_r)
    return st.plotly_chart(fig_sa)

def ques6():
    sa= map_user_df[["States", "AppOpens"]]
    sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=True)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "States", y= "AppOpens", title="lowest 10 States With AppOpens",
                color_discrete_sequence= px.colors.sequential.dense_r)
    return st.plotly_chart(fig_sa)

def ques7():
    stc= aggregated_transaction_df[["States", "Transaction_count"]]
    stc1= stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=True)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "States", y= "Transaction_count", title= "STATES WITH LOWEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Jet_r)
    return st.plotly_chart(fig_stc)

def ques8():
    stc= aggregated_transaction_df[["States", "Transaction_count"]]
    stc1= stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=False)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "States", y= "Transaction_count", title= "STATES WITH HIGHEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Magenta_r)
    return st.plotly_chart(fig_stc)

def ques9():
    ht= aggregated_transaction_df[["States", "Transaction_amount"]]
    ht1= ht.groupby("States")["Transaction_amount"].sum().sort_values(ascending= False)
    ht2= pd.DataFrame(ht1).reset_index().head(10)

    fig_Low_transs= px.bar(ht2, x= "States", y= "Transaction_amount",title= "HIGHEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_Low_transs)

def ques10():
    dt= map_transaction_df[["Districts", "Transaction_amount"]]
    dt1= dt.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=True)
    dt2= pd.DataFrame(dt1).reset_index().head(50)

    fig_dt= px.bar(dt2, x= "Districts", y= "Transaction_amount", title= "DISTRICTS WITH LOWEST TRANSACTION AMOUNT",
                color_discrete_sequence= px.colors.sequential.Mint_r)
    return st.plotly_chart(fig_dt)




mydb =psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe_data",
                        password="mani94")
cursor = mydb.cursor()


def top_chart_transaction_amount(table_name):
    
    #plot_1
    query1= f'''SELECT states, SUM(transaction_amount) AS transaction_amount
                    FROM {table_name}
                    GROUP BY states
                    ORDER BY transaction_amount DESC
                    LIMIT 10;'''

    cursor.execute(query1)
    table= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table, columns=("states", "transaction_amount"))
    col1,col2= st.columns(2)
    with col1:
                fig_amount_1= px.bar(df_1, x="states", y="transaction_amount", title="TOP 10 OF TRANSACTION AMOUNT", hover_name= "states",
                                        color_discrete_sequence=px.colors.sequential.Mint_r, height= 650,width= 600)
                st.plotly_chart(fig_amount_1)


    #plot_2

    query2= f'''SELECT states, SUM(transaction_amount) AS transaction_amount
                    FROM {table_name}
                    GROUP BY states
                    ORDER BY transaction_amount
                    LIMIT 10;'''

    cursor.execute(query2)
    table= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table, columns=("states", "transaction_amount"))
    
    with col2:
        fig_amount_2= px.bar(df_2, x="states", y="transaction_amount", title="LAST 10 OF TRANSACTION AMOUNT", hover_name= "states",
                                color_discrete_sequence=px.colors.sequential.Brwnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3=f'''SELECT states, AVG(transaction_amount) AS transaction_amount
                                FROM {table_name}
                                GROUP BY states
                                ORDER BY transaction_amount;'''

    cursor.execute(query3)
    table= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table, columns=("states", "transaction_amount"))
    fig_amount_3= px.bar(df_3, y="states", x="transaction_amount", title="AVERAGE OF TRANSACTION AMOUNT", orientation="h",hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Blues_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)


    
def top_chart_transaction_count(table_name):
    mydb =psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe_data",
                        password="mani94")
    cursor = mydb.cursor()
    #plot_1
    query1= f'''SELECT districts, SUM(transaction_count) AS transaction_count
                                FROM {table_name}
                                GROUP BY states
                                ORDER BY transaction_count DESC
                                LIMIT 10;'''

    cursor.execute(query1)
    table= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table, columns=("states", "transaction_count"))
    col1,col2= st.columns(2)
    with col1:
                fig_count_1= px.bar(df_1, x="states", y="transaction_count", title=" TOP 10 OF TRANSACTION COUNT", hover_name= "states",
                                        color_discrete_sequence=px.colors.sequential.Greens_r, height= 650,width= 600)
                st.plotly_chart(fig_count_1)


    #plot_2

    query2= f'''SELECT districts, SUM(transaction_count) AS transaction_count
                    FROM {table_name}
                    GROUP BY states
                    ORDER BY transaction_count
                    LIMIT 10;'''

    cursor.execute(query2)
    table= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table, columns=("states", "transaction_count"))
    
    with col2:
        fig_count_2= px.bar(df_2, x="states", y="transaction_count", title="LAST 10 OF TRANSACTION COUNT", hover_name= "states",
                                color_discrete_sequence=px.colors.sequential.Bluyl_r, height= 650,width= 600)
        st.plotly_chart(fig_count_2)

    #plot_3
    query3=f'''SELECT districts, AVG(transaction_count) AS transaction_count
                                FROM {table_name}
                                GROUP BY states
                                ORDER BY transaction_count;'''

    cursor.execute(query3)
    table= cursor.fetchall()
    mydb.commit()
    df_3= pd.DataFrame(table, columns=("states", "transaction_count"))
    fig_count_3 = px.bar(df_3, y="states", x="transaction_count", title=" AVERAGE OF TRANSACTION COUNT", orientation="h",
                     hover_name="states",
                     color_discrete_sequence=px.colors.sequential.Bluered_r,
                     height=800, width=1000)
    st.plotly_chart(fig_count_3)
    




    
def top_chart_transaction_count(table_name):
    mydb =psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe_data",
                        password="mani94")
    cursor = mydb.cursor()
    #plot_1
    query1= f'''SELECT states, SUM(transaction_count) AS transaction_count
                    FROM {table_name}
                    GROUP BY states
                    ORDER BY transaction_count DESC
                    LIMIT 10;'''

    cursor.execute(query1)
    table= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table, columns=("states", "transaction_count"))
    col1,col2= st.columns(2)
    with col1:
                fig_count_1= px.bar(df_1, x="states", y="transaction_count", title="TRANSACTION COUNT", hover_name= "states",
                                        color_discrete_sequence=px.colors.sequential.Greens_r, height= 650,width= 600)
                st.plotly_chart(fig_count_1)


    #plot_2

    query2= f'''SELECT states, SUM(transaction_count) AS transaction_count
                    FROM {table_name}
                    GROUP BY states
                    ORDER BY transaction_count
                    LIMIT 10;'''

    cursor.execute(query2)
    table= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table, columns=("states", "transaction_count"))
    
    with col2:
        fig_count_2= px.bar(df_2, x="states", y="transaction_count", title="TRANSACTION COUNT", hover_name= "states",
                                color_discrete_sequence=px.colors.sequential.Bluyl_r, height= 650,width= 600)
        st.plotly_chart(fig_count_2)

    #plot_3
    query3=f'''SELECT states, AVG(transaction_count) AS transaction_count
                                FROM {table_name}
                                GROUP BY states
                                ORDER BY transaction_count;'''

    cursor.execute(query3)
    table= cursor.fetchall()
    mydb.commit()
    df_3= pd.DataFrame(table, columns=("states", "transaction_count"))
    fig_count_3 = px.bar(df_3, y="states", x="transaction_count", title="TRANSACTION COUNT", orientation="h",
                     hover_name="states",
                     color_discrete_sequence=px.colors.sequential.Bluered_r,
                     height=800, width=1000)
    st.plotly_chart(fig_count_3)
    


   
def top_chart_registered_user(table_name,state):
    mydb =psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe_data",
                        password="mani94")
    cursor = mydb.cursor()
    #plot_1
    query1= f'''SELECT districts, SUM(registeredusers) AS registeredusers
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY registeredusers DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table, columns=("districts", "registeredusers"))
    col1,col2= st.columns(2)
    with col1:
                fig_count_1= px.bar(df_1, x="districts", y="registeredusers", title="TOP 10 REGISTERED USER", hover_name= "districts",
                                        color_discrete_sequence=px.colors.sequential.Greens_r, height= 650,width= 600)
                st.plotly_chart(fig_count_1)


    #plot_2

    query2= f'''SELECT districts, SUM(registeredusers) AS registeredusers
                    FROM {table_name}
                    WHERE states= '{state}'
                    GROUP BY districts
                    ORDER BY registeredusers
                    LIMIT 10;'''

    cursor.execute(query2)
    table= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table, columns=("districts", "registeredusers"))
    
    with col2:
        fig_count_2= px.bar(df_2, x="districts", y="registeredusers", title="LAST 10 REGISTERED USER", hover_name= "districts",
                                color_discrete_sequence=px.colors.sequential.Bluyl_r, height= 650,width= 600)
        st.plotly_chart(fig_count_2)

    #plot_3
    query3=f'''SELECT districts, AVG(registeredusers) AS registeredusers
                                FROM {table_name}
                                WHERE states= '{state}'
                                GROUP BY districts
                                ORDER BY registeredusers;'''

    cursor.execute(query3)
    table= cursor.fetchall()
    mydb.commit()
    df_3= pd.DataFrame(table, columns=("districts", "registeredusers"))
    fig_count_3 = px.bar(df_3, y="districts", x="registeredusers", title="AVERAGE REGISTERED USER", orientation="h",
                     hover_name="districts",
                     color_discrete_sequence=px.colors.sequential.Bluered_r,
                     height=800, width=1000)
    st.plotly_chart(fig_count_3)
    

   
def top_chart_appopens(table_name,state):
    mydb =psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe_data",
                        password="mani94")
    cursor = mydb.cursor()
    #plot_1
    query1= f'''SELECT districts, SUM(appopens) AS appopens
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY appopens DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table, columns=("districts", "appopens"))
    col1,col2= st.columns(2)
    with col1:
                fig_count_1= px.bar(df_1, x="districts", y="appopens", title="TOP 10 APP OPENS", hover_name= "districts",
                                        color_discrete_sequence=px.colors.sequential.Greens_r, height= 650,width= 600)
                st.plotly_chart(fig_count_1)


    #plot_2

    query2= f'''SELECT districts, SUM(appopens) AS appopens
                    FROM {table_name}
                    WHERE states= '{state}'
                    GROUP BY districts
                    ORDER BY appopens
                    LIMIT 10;'''

    cursor.execute(query2)
    table= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table, columns=("districts", "appopens"))
    
    with col2:
        fig_count_2= px.bar(df_2, x="districts", y="appopens", title="LAST 10 APP OPENS", hover_name= "districts",
                                color_discrete_sequence=px.colors.sequential.Bluyl_r, height= 650,width= 600)
        st.plotly_chart(fig_count_2)

    #plot_3
    query3=f'''SELECT districts, AVG(appopens) AS appopens
                                FROM {table_name}
                                WHERE states= '{state}'
                                GROUP BY districts
                                ORDER BY appopens;'''

    cursor.execute(query3)
    table= cursor.fetchall()
    mydb.commit()
    df_3= pd.DataFrame(table, columns=("districts", "appopens"))
    fig_count_3 = px.bar(df_3, y="districts", x="appopens", title="AVERAGE APP OPENS", orientation="h",
                     hover_name="districts",
                     color_discrete_sequence=px.colors.sequential.Bluered_r,
                     height=800, width=1000)
    st.plotly_chart(fig_count_3)
    

   
def top_chart_registered_users(table_name):
    mydb =psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe_data",
                        password="mani94")
    cursor = mydb.cursor()
    #plot_1
    query1= f'''SELECT states, SUM(registeredusers) AS registeredusers
                FROM {table_name}
                GROUP BY states
                ORDER BY registeredusers DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table, columns=("states", "registeredusers"))
    col1,col2= st.columns(2)
    with col1:
                fig_count_1= px.bar(df_1, x="states", y="registeredusers", title="TOP 10 REGISTERED USER", hover_name= "states",
                                        color_discrete_sequence=px.colors.sequential.Blackbody_r, height= 650,width= 600)
                st.plotly_chart(fig_count_1)


    #plot_2

    query2= f'''SELECT states, SUM(registeredusers) AS registeredusers
                    FROM top_user
                    GROUP BY states
                    ORDER BY registeredusers
                    LIMIT 10;'''

    cursor.execute(query2)
    table= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table, columns=("states", "registeredusers"))
    
    with col2:
        fig_count_2= px.bar(df_2, x="states", y="registeredusers", title="LAST 10 REGISTERED USER", hover_name= "states",
                                color_discrete_sequence=px.colors.sequential.Redor_r, height= 650,width= 600)
        st.plotly_chart(fig_count_2)

    #plot_3
    query3=f'''SELECT states, AVG(registeredusers) AS registeredusers
                                FROM top_user
                                GROUP BY states
                                ORDER BY registeredusers;'''

    cursor.execute(query3)
    table= cursor.fetchall()
    mydb.commit()
    df_3= pd.DataFrame(table, columns=("states", "registeredusers"))
    fig_count_3 = px.line(df_3, x="states", y="registeredusers", title="AVERAGE REGISTERED USER",
                      color_discrete_sequence=px.colors.sequential.YlGnBu_r,
                      height=800, width=1000)
    st.plotly_chart(fig_count_3)





#streamlit Part


st.set_page_config(layout= "wide")

st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")
st.write("")

with st.sidebar:
    select= option_menu("Main Menu",["Home", "Data Exploration", "Top Charts"])


if select == "Home":

    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe is an Indian digital payments and financial technology company.")

        # Features
        st.write("****FEATURES****")
        st.write("1. **Credit & Debit Card Linking**: Seamlessly connect your cards for easy transactions.")
        st.write("2. **Bank Balance Check**: Effortlessly monitor your account balance.")
        st.write("3. **Money Storage**: Securely store funds within the app.")
        st.write("4. **PIN Authorization**: Ensure safety with personalized PIN protection.")
    
        # Download the App
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        st.image(Image.open(r"C:\Users\manik\Desktop\New folder youtube harvest\phone-pay-image.jpg"),width=400)
    col3,col4=st.columns(2)
    with col3:    
        st.image(Image.open(r"C:\Users\manik\Desktop\New folder youtube harvest\PP_LogoSectionDivider.jpg"),width=350)

    with col4:
        st.header("Features of PhonePe")
        st.write("1. Credit and Debit Card Linking")
        st.write("2. Bank Balance Check")
        st.write("3. Money Storage")
        st.write("4. App to Bank Account")
        st.write("5. Send and Receive Money")
        st.write("6. POS Payments")
        st.write("7. PIN Authorization")
        st.write("8. Wallet Top-Ups")

        st.header("Benefits of PhonePe")
    
        st.write("- All-in-One Solution")
        st.write("- Direct Fund Transfers")
        st.write("- Multiple Payment Options")
        st.write("- Multi-Language Interface")
        st.write("- Intuitive POS")
            






if select == "Home":
    pass

elif select =="Data Exploration":
        
        tab1,tab2,tab3 = st.tabs(["Aggregated Analysis","Map Analysis","Top Analysis"])
   
        with tab1:
            method=st.radio("Select the Method",["Insurance Analysis","Transaction Analysis","User Analysis"]) 
          
            if method == "Insurance Analysis":
            
                col1,col2=st.columns(2)  

                with col1:

                    years=st.slider("Select The Year",aggregated_insurance_df["Years"].max(),aggregated_insurance_df["Years"].min())
                    
                    tac_Y=Transaction_Amount_Count_Year(aggregated_insurance_df,years)

                col1,col2=st.columns(2)  

                with col1:
                        quarter=st.slider("Select The Quarter",tac_Y["Quarter"].max(),tac_Y["Quarter"].min())
                        
                Transaction_Amount_Count_Year_Quarter(tac_Y,quarter)


            elif method == "Transaction Analysis":
                    col1,col2= st.columns(2)
                    with col1:
                        cursor.execute("SELECT * FROM aggregated_transaction")

                        aggregated_transaction_df = pd.DataFrame(aggregated_transaction_data, columns=
                                         ("States", "Years", "Quarter", "Transaction_type",
                                          "Transaction_count", "Transaction_amount"))
                        years= st.slider("**Select the Year**", aggregated_transaction_df["Years"].max(), aggregated_transaction_df["Years"].min())

                    aggre_tran_tac_Y= Transaction_Amount_Count_Year(aggregated_transaction_df,years)
                    

                    col1,col2= st.columns(2)
                    with col1:
                         
                        states= st.selectbox("**Select the State**",aggre_tran_tac_Y["States"].unique())

                        Aggre_Trans_Transaction_type(aggre_tran_tac_Y, states)

                    col1,col2=st.columns(2)  

                    with col1:
                            quarter=st.slider("Select The Quarter",aggre_tran_tac_Y["Quarter"].min(),aggre_tran_tac_Y["Quarter"].max(),aggre_tran_tac_Y["Quarter"].min())
                            
                            aggre_tran_tac_Y_Q = Transaction_Amount_Count_Year_Quarter(aggre_tran_tac_Y,quarter)

                    col1,col2= st.columns(2)
                    with col1:
                        states= st.selectbox("**Select the State_Ty**",aggre_tran_tac_Y_Q["States"].unique())

                        Aggre_Trans_Transaction_type(aggre_tran_tac_Y, states)



            
            elif method == "User Analysis":
                    year_au= st.selectbox("Select the Year_AU",aggregated_user_df["Years"].unique())
                    agg_user_Y= Aggre_user_plot_1(aggregated_user_df,year_au)

                    quarter_au= st.selectbox("Select the Quarter_AU",agg_user_Y["Quarter"].unique())
                    agg_user_Y_Q= Aggre_user_plot_2(agg_user_Y,quarter_au)

                    state_au= st.selectbox("**Select the State_AU**",agg_user_Y["States"].unique())
                    Aggre_user_plot_3(agg_user_Y_Q,state_au)

        with tab2:
            method_map = st.radio("**Select the Analysis Method(MAP)**",["Map Insurance Analysis", "Map Transaction Analysis", "Map User Analysis"])

            if method_map == "Map Insurance Analysis":
                col1,col2= st.columns(2)
                with col1:
                    years_m1= st.slider("**Select the Year_mi**", map_insurance_df["Years"].min(), map_insurance_df["Years"].max(),map_insurance_df["Years"].min())

                df_map_insur_Y= Transaction_Amount_Count_Year(map_insurance_df,years_m1)

                col1,col2= st.columns(2)
                with col1:
                    state_m1= st.selectbox("Select the State_mi", df_map_insur_Y["States"].unique())

                map_insure_plot_1(df_map_insur_Y,state_m1)
                
                col1,col2= st.columns(2)
                with col1:
                    quarters_m1= st.slider("**Select the Quarter_mi**", df_map_insur_Y["Quarter"].min(), df_map_insur_Y["Quarter"].max(),df_map_insur_Y["Quarter"].min())

                df_map_insur_Y_Q= Transaction_Amount_Count_Year_Quarter(df_map_insur_Y, quarters_m1)

                col1,col2= st.columns(2)
                with col1:
                    state_m2= st.selectbox("Select the State_miy", df_map_insur_Y_Q["States"].unique())            
                
                map_insure_plot_2(df_map_insur_Y_Q, state_m2)

            elif method_map == "Map Transaction Analysis":
                col1,col2= st.columns(2)
                with col1:
                    years_m2= st.slider("**Select the Year_mi**", map_transaction_df["Years"].min(), map_transaction_df["Years"].max(),map_transaction_df["Years"].min())

                df_map_tran_Y= Transaction_Amount_Count_Year(map_transaction_df, years_m2)

                col1,col2= st.columns(2)
                with col1:
                    state_m3= st.selectbox("Select the State_mi", df_map_tran_Y["States"].unique())

                map_insure_plot_1(df_map_tran_Y,state_m3)
                
                col1,col2= st.columns(2)
                with col1:
                    quarters_m2= st.slider("**Select the Quarter_mi**", df_map_tran_Y["Quarter"].min(), df_map_tran_Y["Quarter"].max(),df_map_tran_Y["Quarter"].min())

                df_map_tran_Y_Q= Transaction_Amount_Count_Year_Quarter(df_map_tran_Y, quarters_m2)

                col1,col2= st.columns(2)
                with col1:
                    state_m4= st.selectbox("Select the State_miy", df_map_tran_Y_Q["States"].unique())            
                
                map_insure_plot_2(df_map_tran_Y_Q, state_m4)

            elif method_map == "Map User Analysis":
                col1,col2= st.columns(2)
                with col1:
                    year_mu1= st.selectbox("**Select the Year_mu**",map_user_df["Years"].unique())
                map_user_Y= map_user_plot_1(map_user_df, year_mu1)

                col1,col2= st.columns(2)
                with col1:
                    quarter_mu1= st.selectbox("**Select the Quarter_mu**",map_user_Y["Quarter"].unique())
                map_user_Y_Q= map_user_plot_2(map_user_Y,quarter_mu1)

                col1,col2= st.columns(2)
                with col1:
                    state_mu1= st.selectbox("**Select the State_mu**",map_user_Y_Q["States"].unique())
                map_user_plot_3(map_user_Y_Q, state_mu1)

        with tab3:
            method_top = st.radio("**Select the Analysis Method(TOP)**",["Top Insurance Analysis", "Top Transaction Analysis", "Top User Analysis"])

            if method_top == "Top Insurance Analysis":
                col1,col2= st.columns(2)
                with col1:
                    years_t1= st.slider("**Select the Year_ti**", top_insurance_df["Years"].min(), top_insurance_df["Years"].max(),top_insurance_df["Years"].min())
    
                df_top_insur_Y= Transaction_Amount_Count_Year(top_insurance_df,years_t1)

                
                col1,col2= st.columns(2)
                with col1:
                    quarters_t1= st.slider("**Select the Quarter_ti**", df_top_insur_Y["Quarter"].min(), df_top_insur_Y["Quarter"].max(),df_top_insur_Y["Quarter"].min())

                df_top_insur_Y_Q= Transaction_Amount_Count_Year_Quarter(df_top_insur_Y, quarters_t1)

        
            elif method_top == "Top Transaction Analysis":
                col1,col2= st.columns(2)
                with col1:
                    years_t2= st.slider("**Select the Year_tt**", top_transaction_df["Years"].min(), top_transaction_df["Years"].max(),top_transaction_df["Years"].min())
    

         
            elif method_top == "Top User Analysis":
                    col1, col2 = st.columns(2)

                    # User registration analysis
                    with col1:
                        year_tu = st.selectbox("Select the Year (User Registration)", top_user_df["Years"].unique())
                        df_top_user_Y = top_user_plot_1(top_user_df, year_tu)

                        quarter_tu = st.selectbox("Select the Quarter (User Registration)", df_top_user_Y["Quarter"].unique())
                        df_top_user_Y_Q = top_user_plot_2(df_top_user_Y, quarter_tu)

                    # App opens analysis
                    with col2:
                        state_tu = st.selectbox("Select the State (App Opens)", df_top_user_Y["States"].unique())
                        top_user_plot_2(df_top_user_Y_Q, state_tu)


            elif method_top == "Top Transaction Analysis":
                col1, col2 = st.columns(2)

                # Transaction amount analysis
                with col1:
                    years_t2 = st.slider("Select the Year (Transaction Amount)", top_transaction_df["Years"].min(), top_transaction_df["Years"].max(), top_transaction_df["Years"].min())
                    df_top_tran_Y = Transaction_Amount_Count_Year(top_transaction_df, years_t2)

                    quarters_t2 = st.slider("Select the Quarter (Transaction Amount)", df_top_tran_Y["Quarter"].min(), df_top_tran_Y["Quarter"].max(), df_top_tran_Y["Quarter"].min())
                    df_top_tran_Y_Q = Transaction_Amount_Count_Year_Quarter(df_top_tran_Y, quarters_t2)

                # Transaction count analysis
                with col2:
                    state_t3 = st.selectbox("Select the State (Transaction Count)", df_top_tran_Y_Q["States"].unique())
                    Aggre_Trans_Transaction_type(df_top_tran_Y, state_t3)



            elif method_top == "Top Insurance Analysis":
                col1, col2 = st.columns(2)

                # Transaction amount analysis
                with col1:
                    years_t1 = st.slider("Select the Year (Transaction Amount)", top_insurance_df["Years"].min(), top_insurance_df["Years"].max(), top_insurance_df["Years"].min())
                    df_top_insur_Y = Transaction_Amount_Count_Year(top_insurance_df, years_t1)

                    quarters_t1 = st.slider("Select the Quarter (Transaction Amount)", df_top_insur_Y["Quarter"].min(), df_top_insur_Y["Quarter"].max(), df_top_insur_Y["Quarter"].min())
                    df_top_insur_Y_Q = Transaction_Amount_Count_Year_Quarter(df_top_insur_Y, quarters_t1)

                # Transaction count analysis
                with col2:
                    state_t1 = st.selectbox("Select the State (Transaction Count)", df_top_insur_Y_Q["States"].unique())
                    Aggre_Trans_Transaction_type(df_top_insur_Y, state_t1)


            elif method_map == "Map Transaction Analysis":
                col1, col2 = st.columns(2)

                # Transaction amount analysis
                with col1:
                    years_m2 = st.slider("Select the Year (Transaction Amount)", map_transaction_df["Years"].min(), map_transaction_df["Years"].max(), map_transaction_df["Years"].min())
                    df_map_tran_Y = Transaction_Amount_Count_Year(map_transaction_df, years_m2)

                    state_m3 = st.selectbox("Select the State (Transaction Amount)", df_map_tran_Y["States"].unique())
                    map_insure_plot_1(df_map_tran_Y, state_m3)

                # Transaction count analysis
                with col2:
                    quarters_m2 = st.slider("Select the Quarter (Transaction Count)", df_map_tran_Y["Quarter"].min(), df_map_tran_Y["Quarter"].max(), df_map_tran_Y["Quarter"].min())
                    df_map_tran_Y_Q = Transaction_Amount_Count_Year_Quarter(df_map_tran_Y, quarters_m2)

                    state_m4 = st.selectbox("Select the State (Transaction Count)", df_map_tran_Y_Q["States"].unique())
                    map_insure_plot_2(df_map_tran_Y_Q, state_m4)

           
            elif method_map == "Map User Analysis":
                col1, col2 = st.columns(2)

                # User registration analysis
                with col1:
                    year_mu1 = st.selectbox("Select the Year (User Registration)", map_user_df["Years"].unique())
                    map_user_Y = map_user_plot_1(map_user_df, year_mu1)

                    quarter_mu1 = st.selectbox("Select the Quarter (User Registration)", map_user_Y["Quarter"].unique())
                    map_user_Y_Q = map_user_plot_2(map_user_Y, quarter_mu1)

                # App opens analysis
                with col2:
                    state_mu1 = st.selectbox("Select the State (App Opens)", map_user_Y["States"].unique())
                    map_user_plot_3(map_user_Y_Q, state_mu1)


elif select == "Top Charts":
        question = st.selectbox("Select the Question", [
            "1. Transaction Amount and Count of Aggregated Insurance",
            "2. Transaction Amount and Count of Aggregated Transaction",
            "3. Transaction Amount and Count of Map Insurance",
            "4. Transaction Amount and Count of Map Transaction",
            "5. Transaction Amount and Count of Top Insurance",
            "6. Transaction Amount and Count of Top Transaction",
            "7. Transaction Count of Aggregated User",
            "8. Registered users of Map User",
            "9. App opens of Map User",
            "10. Registered users of Top User",
              ])
        if question == "1. Transaction Amount and Count of Aggregated Insurance":

            st.subheader("TRANSACTION AMOUNT")
            top_chart_transaction_amount("aggregated_insurance")

            st.subheader("TRANSACTION COUNT")
            top_chart_transaction_count("aggregated_insurance")

        elif question == "2. Transaction Amount and Count of Aggregated Transaction":

            st.subheader("TRANSACTION AMOUNT")
            top_chart_transaction_amount("aggregated_transaction")

            st.subheader("TRANSACTION COUNT")
            top_chart_transaction_count("aggregated_transaction")   

            
        elif question == "3. Transaction Amount and Count of Map Insurance":

            st.subheader("TRANSACTION AMOUNT")
            top_chart_transaction_amount("map_insurance")

            st.subheader("TRANSACTION COUNT")
            top_chart_transaction_count("map_insurance")

        elif question == "4. Transaction Amount and Count of Map Transaction":

            st.subheader("TRANSACTION AMOUNT")
            top_chart_transaction_amount("map_transaction")

            st.subheader("TRANSACTION COUNT")
            top_chart_transaction_count("map_transaction")  


        elif question == "5. Transaction Amount and Count of Top Insurance":

            st.subheader("TRANSACTION AMOUNT")
            top_chart_transaction_amount("top_insurance")

            st.subheader("TRANSACTION COUNT")
            top_chart_transaction_count("top_insurance")

        elif question == "6. Transaction Amount and Count of Top Transaction":

            st.subheader("TRANSACTION AMOUNT")
            top_chart_transaction_amount("top_transaction")

            st.subheader("TRANSACTION COUNT")
            top_chart_transaction_count("top_transaction")   

        elif question == "7. Transaction Count of Aggregated User":

           
            st.subheader("TRANSACTION COUNT")
            top_chart_transaction_count("aggregated_user")

        elif question == "8. Registered users of Map User":

            states= st.selectbox("Select the State", map_user_df["States"].unique())
            st.subheader("REGISTERED USERS")
            top_chart_registered_user("map_user", states)


        elif question == "9. App opens of Map User":
            
            states= st.selectbox("Select the State", map_user_df["States"].unique())
            st.subheader("APP OPENS")
            top_chart_appopens("map_user", states)


        elif question == "10. Registered users of Top User":

            st.subheader("APP OPENS")
            top_chart_registered_users("top_user")