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
    fig, axes = plt.subplots(2, 2, figsize=(18, 12))

    day_df_grouped = day_df.groupby('weathersit', as_index=False)['total_rentals'].sum().sort_values(by='total_rentals', ascending=False)
    hour_df_grouped = hour_df.groupby('weathersit', as_index=False)['total_rentals'].sum().sort_values(by='total_rentals', ascending=False)

    sns.barplot(
        x='weathersit', 
        y='total_rentals', 
        hue='weathersit',  
        data=day_df_grouped, 
        ax=axes[0, 0], 
        palette='viridis',
        legend=False
    )
    axes[0, 0].set_title('Total Rentals per Weather Condition (Day)')
    axes[0, 0].set_xlabel('Weather Condition')
    axes[0, 0].set_ylabel('Total Rentals')

    sns.barplot(
        x='weathersit', 
        y='total_rentals', 
        hue='weathersit',  
        data=hour_df_grouped, 
        ax=axes[0, 1], 
        palette='magma',
        legend=False
    )
    axes[0, 1].set_title('Total Rentals per Weather Condition (Hour)')
    axes[0, 1].set_xlabel('Weather Condition')
    axes[0, 1].set_ylabel('Total Rentals')

    sns.boxplot(
        x='weathersit', 
        y='total_rentals', 
        data=day_df, 
        ax=axes[1, 0], 
        palette='coolwarm'
    )
    axes[1, 0].set_title('Rental Distribution per Weather Condition (Day)')
    axes[1, 0].set_xlabel('Weather Condition')
    axes[1, 0].set_ylabel('Total Rentals')

    sns.boxplot(
        x='weathersit', 
        y='total_rentals', 
        data=hour_df, 
        ax=axes[1, 1], 
        palette='rocket'
    )
    axes[1, 1].set_title('Rental Distribution per Weather Condition (Hour)')
    axes[1, 1].set_xlabel('Weather Condition')
    axes[1, 1].set_ylabel('Total Rentals')

    plt.tight_layout()
    return fig


import seaborn as sns
import matplotlib.pyplot as plt

def plot_rentals_analysis(day_df, hour_df):
    sns.set_theme(style="whitegrid", palette="muted")
    plt.rcParams.update({'font.size': 11})
    
    hari_mapping = {
        'Sunday': 6,
        'Monday': 0,
        'Tuesday': 1,
        'Wednesday': 2,
        'Thursday': 3,
        'Friday': 4,
        'Saturday': 5
    }
    
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
    
    num_plots = sum([
        not tipe_hari_data.empty,
        not weekday_data.empty,
        not hourly_data_plot.empty
    ])
    
    fig, axes = plt.subplots(nrows=num_plots, ncols=1, figsize=(12, 6*num_plots))
    
    if num_plots == 1:
        axes = [axes]
    
    plot_index = 0
    
    if not tipe_hari_data.empty:
        sns.barplot(x='tipe_hari', y='total_rentals', data=tipe_hari_data, ax=axes[plot_index])
        axes[plot_index].set_title('Perbandingan Volume Penyewaan: Hari Kerja vs Hari Libur', fontsize=14, fontweight='bold')
        axes[plot_index].set_ylabel('Total Penyewaan')
        axes[plot_index].set_xlabel('')

        for i, row in tipe_hari_data.iterrows():
            axes[plot_index].text(i, row['total_rentals'] + (tipe_hari_data['total_rentals'].max() * 0.02), 
                             f'{int(row["total_rentals"]):,} ({row["persentase"]}%)',
                             ha='center')
        plot_index += 1
    
    if not weekday_data.empty:
        sns.lineplot(x='weekday_num', y='total_rentals', data=weekday_data, marker='o', linewidth=2.5, color='#2ca02c', ax=axes[plot_index])
        axes[plot_index].set_xticks(range(min(7, len(weekday_data))))
        axes[plot_index].set_xticklabels([hari_names[i] for i in weekday_data['weekday_num'] if i < len(hari_names)])
        
        for i, row in weekday_data.iterrows():
            axes[plot_index].text(row['weekday_num'], row['total_rentals'] + (weekday_data['total_rentals'].max() * 0.03), 
                             f'{int(row["total_rentals"]):,}', ha='center')
        
        axes[plot_index].set_title('Pola Penyewaan Sepeda Selama Seminggu', fontsize=14, fontweight='bold')
        axes[plot_index].set_ylabel('Total Penyewaan')
        axes[plot_index].set_xlabel('')
        plot_index += 1

    if not hourly_data_plot.empty:
        tipe_hari_counts = hourly_data_plot['tipe_hari'].nunique()
        
        if tipe_hari_counts > 1:
            sns.lineplot(x='hour', y='total_rentals', hue='tipe_hari', data=hourly_data_plot, marker='o', 
                     palette=['#1f77b4', '#ff7f0e'], ax=axes[plot_index])
        else:
            sns.lineplot(x='hour', y='total_rentals', data=hourly_data_plot, marker='o', color='#1f77b4', ax=axes[plot_index])
        
        hours_available = hourly_data_plot['hour'].unique()
        if any(7 <= h <= 9 for h in hours_available):
            axes[plot_index].axvspan(7, 9, alpha=0.2, color='red', label='Jam Sibuk Pagi')
        if any(16 <= h <= 18 for h in hours_available):
            axes[plot_index].axvspan(16, 18, alpha=0.2, color='green', label='Jam Sibuk Sore')
        
        axes[plot_index].set_title('Pola Penyewaan Per Jam: Hari Kerja vs Hari Libur', fontsize=14, fontweight='bold')
        axes[plot_index].set_ylabel('Jumlah Penyewaan')
        axes[plot_index].set_xlabel('Jam')
        
        available_hours = sorted(hourly_data_plot['hour'].unique())
        if available_hours:
            axes[plot_index].set_xticks(available_hours)
        
        if tipe_hari_counts > 1:
            axes[plot_index].legend(title='')
        
    fig.suptitle('Analisis Pola Penyewaan Sepeda', fontsize=16, fontweight='bold', y=0.98)
    
    if num_plots > 1:
        fig.text(0.5, 0.01, 'Penyewaan pada hari kerja lebih tinggi dari hari libur, dengan puncak pada jam sibuk', 
             ha='center', fontsize=12, fontstyle='italic')
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.95, bottom=0.07)
    
    return fig

def plot_rentals_by_time_of_day(hour_df):
    try:
        if hour_df.empty:
            plt.figure(figsize=(10, 6))
            plt.text(0.5, 0.5, "Tidak ada data untuk divisualisasikan", 
                    ha='center', va='center', fontsize=14)
            plt.tight_layout()
            return plt.gcf()
        
        required_cols = ["time_of_day", "total_rentals"]
        if not all(col in hour_df.columns for col in required_cols):
            plt.figure(figsize=(10, 6))
            plt.text(0.5, 0.5, "Data tidak memiliki kolom yang diperlukan (time_of_day, total_rentals)", 
                    ha='center', va='center', fontsize=14)
            plt.tight_layout()
            return plt.gcf()
        
        colors = ['#8dd3c7', '#bebada', '#fb8072', '#80b1d3']
        
        time_group = hour_df.groupby("time_of_day")["total_rentals"].sum().reset_index()
        time_order = ["Morning", "Afternoon", "Evening", "Night"]
        available_periods = set(time_group["time_of_day"].unique())
        time_order = [period for period in time_order if period in available_periods]
        
        if not time_order:
            plt.figure(figsize=(10, 6))
            plt.text(0.5, 0.5, "Data tidak memiliki kategori waktu yang valid", 
                    ha='center', va='center', fontsize=14)
            plt.tight_layout()
            return plt.gcf()
        
        time_group = time_group.set_index("time_of_day").reindex(time_order).reset_index()
        
        time_labels = {
            "Morning": "Morning (06:00-12:00)",
            "Afternoon": "Afternoon (12:00-18:00)",
            "Evening": "Evening (18:00-00:00)",
            "Night": "Night (00:00-06:00)"
        }
        
        display_labels = [time_labels.get(period, period) for period in time_order]
    
        plt.figure(figsize=(10, 6))
        
        if len(time_order) == 1:
            ax = sns.barplot(
                x="total_rentals",
                y="time_of_day",
                data=time_group,
                color=colors[time_order.index(time_order[0]) % len(colors)],
                orient='h'
            )
        else:
            custom_palette = {period: colors[i % len(colors)] for i, period in enumerate(time_order)}
            
            ax = sns.barplot(
                x="total_rentals",
                y="time_of_day",
                data=time_group,
                palette=custom_palette,
                orient='h'
            )
        
        for index, value in enumerate(time_group["total_rentals"]):
            ax.text(value, index, f'{value:,.0f}', va='center', fontsize=12)
        
        from matplotlib.ticker import FuncFormatter
        formatter = FuncFormatter(lambda x, pos: f'{int(x):,}')
        ax.xaxis.set_major_formatter(formatter)
        
        plt.title("Total Penyewaan Sepeda Berdasarkan Waktu dalam Sehari", fontsize=14, fontweight='bold')
        plt.xlabel("Total Penyewaan", fontsize=12, labelpad=15) 
        plt.ylabel("Periode Waktu", fontsize=12, labelpad=15)  
        plt.grid(axis="x", linestyle="--", alpha=0.7)
        plt.yticks(ticks=range(len(display_labels)), labels=display_labels)
        
        if not time_group.empty and len(time_group) > 1:
            highest_period = time_group.loc[time_group["total_rentals"].idxmax(), "time_of_day"]
            lowest_period = time_group.loc[time_group["total_rentals"].idxmin(), "time_of_day"]
            highest_value = time_group["total_rentals"].max()
            lowest_value = time_group["total_rentals"].min()
            
            # if highest_value != lowest_value:
            #     plt.annotate(f"Tertinggi: {highest_value:,.0f}", 
            #                 xy=(highest_value, time_order.index(highest_period)),
            #                 xytext=(highest_value + highest_value*0.05, time_order.index(highest_period) - 0.3),
            #                 arrowprops=dict(arrowstyle="->", color="green", lw=1.5),
            #                 fontsize=11, color="green", fontweight="bold")
                
            #     plt.annotate(f"Terendah: {lowest_value:,.0f}", 
            #                 xy=(lowest_value, time_order.index(lowest_period)),
            #                 xytext=(lowest_value + highest_value*0.05, time_order.index(lowest_period) + 0.3),
            #                 arrowprops=dict(arrowstyle="->", color="red", lw=1.5),
            #                 fontsize=11, color="red", fontweight="bold")
        
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.15)
        
        return plt.gcf()
    
    except Exception as e:
        plt.figure(figsize=(10, 6))
        plt.text(0.5, 0.5, f"Terjadi kesalahan: {str(e)}", 
                ha='center', va='center', fontsize=14)
        plt.tight_layout()
        return plt.gcf()



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