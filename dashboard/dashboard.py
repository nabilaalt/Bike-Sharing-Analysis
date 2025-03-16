import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter
import numpy as np
from datetime import datetime

def configure_page():
    st.set_page_config(
        page_title="Dashboard Penyewaan Sepeda",
        page_icon="🚲",
        layout="wide"
    )
    
    st.markdown("""
    <style>
    .stPlotlyChart, .stPlot {
        background-color: transparent !important;
    }
    .css-1kyxreq, .css-12oz5g7 {
        margin-top: -2rem;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():

    day_df = pd.read_csv("dashboard/cleaned_day_data.csv")
    hour_df = pd.read_csv("dashboard/cleaned_hour_data.csv")
    
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    
    return day_df, hour_df

def plot_weather_comparison(day_df, hour_df):
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))  
    
    day_df_grouped = day_df.groupby('weathersit', as_index=False)['total_rentals'].sum().sort_values(by='total_rentals', ascending=False)
    hour_df_grouped = hour_df.groupby('weathersit', as_index=False)['total_rentals'].sum().sort_values(by='total_rentals', ascending=False)
    
    sns.barplot(
        x='weathersit', 
        y='total_rentals',  
        data=day_df_grouped, 
        ax=axes[0], 
        color="#87CEEB"
    )
    axes[0].set_title('Total Rentals per Weather Condition (Day)', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Weather Condition')
    axes[0].set_ylabel('Total Rentals')
    axes[0].grid(axis='y', linestyle='--', alpha=0.7)
    
    for p in axes[0].containers:
        axes[0].bar_label(p, fmt='%.0f', fontsize=10, padding=3)
    
    sns.barplot(
        x='weathersit', 
        y='total_rentals',  
        data=hour_df_grouped, 
        ax=axes[1], 
        color="#87CEEB"
    )
    axes[1].set_title('Total Rentals per Weather Condition (Hour)', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Weather Condition')
    axes[1].set_ylabel('Total Rentals')
    axes[1].grid(axis='y', linestyle='--', alpha=0.7)
    
    for p in axes[1].containers:
        axes[1].bar_label(p, fmt='%.0f', fontsize=10, padding=3)
    
    plt.tight_layout()
    return fig
def plot_rentals_analysis(day_df, hour_df):
    hari_mapping = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6}
    sns.set_theme(style="whitegrid", palette="muted")
    plt.rcParams.update({'font.size': 11})

    plot_df = day_df.copy()
    plot_df['weekday_num'] = plot_df['weekday'].map(hari_mapping)
    plot_df['tipe_hari'] = plot_df['workingday'].map({'Yes': 'Hari Kerja', 'No': 'Hari Libur'})

    tipe_hari_data = plot_df.groupby('tipe_hari', as_index=False)['total_rentals'].sum()
    tipe_hari_data['persentase'] = (tipe_hari_data['total_rentals'] / tipe_hari_data['total_rentals'].sum() * 100).round(1)

    weekday_data = plot_df.groupby('weekday_num', as_index=False)['total_rentals'].sum()
    hari_names = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
    weekday_data['hari'] = weekday_data['weekday_num'].map(dict(enumerate(hari_names)))

    hourly_data_plot = hour_df.groupby(['hour', 'workingday'], as_index=False)['total_rentals'].sum()
    hourly_data_plot['tipe_hari'] = hourly_data_plot['workingday'].map({'Yes': 'Hari Kerja', 'No': 'Hari Libur'})

    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(12, 18))

    ax = sns.barplot(x='tipe_hari', y='total_rentals', data=tipe_hari_data, ax=axes[0], color="#FFABAB")
    for p, perc in zip(ax.patches, tipe_hari_data['persentase']):
        axes[0].text(p.get_x() + p.get_width()/2., p.get_height() + 1500, 
                     f'{int(p.get_height()):,}\n({perc}%)', 
                     ha="center", fontsize=12)

    axes[0].set_title('Perbandingan Volume Penyewaan: Hari Kerja vs Hari Libur', fontsize=14, fontweight='bold')
    axes[0].set_ylabel('Total Penyewaan')
    axes[0].set_xlabel('')
    axes[0].set_ylim(0, 2500000)  

    sns.lineplot(x='weekday_num', y='total_rentals', data=weekday_data, marker='o', linewidth=2.5, color="#6A5ACD", ax=axes[1])
    axes[1].set_xticks(range(7))
    axes[1].set_xticklabels(hari_names)
    for i, row in weekday_data.iterrows():
        axes[1].text(row['weekday_num'], row['total_rentals'] + 500, f'{int(row["total_rentals"]):,}', ha='center')

    axes[1].set_title('Pola Penyewaan Sepeda Selama Seminggu', fontsize=14, fontweight='bold')
    axes[1].set_ylabel('Total Penyewaan')
    axes[1].set_xlabel('')

    sns.lineplot(x='hour', y='total_rentals', hue='tipe_hari', data=hourly_data_plot, marker='o', palette=['#1f77b4', '#ff7f0e'], ax=axes[2])
    axes[2].axvspan(7, 9, alpha=0.2, color='red', label='Jam Sibuk Pagi')
    axes[2].axvspan(16, 18, alpha=0.2, color='green', label='Jam Sibuk Sore')
    axes[2].set_title('Pola Penyewaan Per Jam: Hari Kerja vs Hari Libur', fontsize=14, fontweight='bold')
    axes[2].set_ylabel('Jumlah Penyewaan')
    axes[2].set_xlabel('Jam')
    axes[2].set_xticks(range(24))
    axes[2].legend(title='')

    fig.suptitle('Analisis Pola Penyewaan Sepeda', fontsize=16, fontweight='bold', y=0.99)
    fig.text(0.5, 0.01, 'Penyewaan pada hari kerja lebih tinggi dari hari libur, dengan puncak pada jam sibuk', ha='center', fontsize=12, fontstyle='italic')

    plt.tight_layout()
    plt.subplots_adjust(top=0.95, bottom=0.05)
    return fig

def plot_rentals_by_time_of_day(hour_df):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    time_group = hour_df.groupby("time_of_day")["total_rentals"].sum().reset_index()
    time_order = ["Morning", "Afternoon", "Evening", "Night"]
    time_group = time_group.set_index("time_of_day").reindex(time_order).reset_index()
    time_labels = ["Morning (06:00-12:00)", "Afternoon (12:00-18:00)", "Evening (18:00-00:00)", "Night (00:00-06:00)"]
    
    sns.barplot(
        x="total_rentals",
        y="time_of_day",
        data=time_group,
        color="#FFA07A",
        orient='h',
        ax=ax
    )
    
    for index, value in enumerate(time_group["total_rentals"]):
        ax.text(value, index, f'{value:,.0f}', va='center', fontsize=12)
    
    formatter = FuncFormatter(lambda x, pos: f'{int(x):,}')
    ax.xaxis.set_major_formatter(formatter)
    
    ax.set_title("Total Penyewaan Sepeda Berdasarkan Waktu dalam Sehari", fontsize=14, fontweight='bold')
    ax.set_xlabel("Total Penyewaan", fontsize=12, labelpad=15)
    ax.set_ylabel("Periode Waktu", fontsize=12, labelpad=15)
    ax.grid(axis="x", linestyle="--", alpha=0.7)
    ax.set_yticks(range(len(time_labels)))
    ax.set_yticklabels(time_labels)
    
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.15)
    return fig

def main():
    configure_page()
    
    st.title("📊 Dashboard Penyewaan Sepeda")
    st.markdown("---")
    
    try:
        day_df, hour_df = load_data()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.warning("Gunakan placeholder data untuk demonstrasi")
        

    st.sidebar.header("Filter Data")
    
    min_date = day_df['dteday'].min().date()
    max_date = day_df['dteday'].max().date()
    
    start_date = st.sidebar.date_input(
        "Tanggal Mulai",
        min_date,
        min_value=min_date,
        max_value=max_date
    )
    
    end_date = st.sidebar.date_input(
        "Tanggal Akhir",
        max_date,
        min_value=start_date,
        max_value=max_date
    )
    
    start_date = pd.Timestamp(start_date)
    end_date = pd.Timestamp(end_date)

    filtered_day_df = day_df[(day_df['dteday'] >= start_date) & (day_df['dteday'] <= end_date)]
    filtered_hour_df = hour_df[(hour_df['dteday'] >= start_date) & (hour_df['dteday'] <= end_date)]
    
    st.header("Perbandingan Penyewaan Sepeda Berdasarkan Kondisi Cuaca")
    weather_comparison_fig = plot_weather_comparison(filtered_day_df, filtered_hour_df)
    st.pyplot(weather_comparison_fig)
    st.markdown("---")

    st.header("Pola Penyewaan Sepeda Berdasarkan hari")
    pattern_day = plot_rentals_analysis(filtered_day_df,filtered_hour_df)
    st.pyplot(pattern_day)
    st.markdown("---")

    st.header("Total Penyewaan Sepeda Berdasarkan Waktu Dalam Sehari")
    pattern_time = plot_rentals_by_time_of_day(filtered_hour_df)
    st.pyplot(pattern_time)
    st.markdown("---")

if __name__ == "__main__":
    main()