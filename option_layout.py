import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import matplotlib.ticker as mticker

import pandas as pd
class OptionLayout:
    prange = 600
    
    def __init__(self) -> None:
        #Create a DF to record option
        self.df_opt = pd.DataFrame(columns=['OPTTYPE', 'POINT', 'UNIT', 'COST'])

    #add option to df_opt
    def add(self, opttype, point, unit, cost) -> None:
        self.df_opt.loc[len(self.df_opt.index)] = [opttype, point, unit, cost]

    #calculator option to df_cal
    def cal(self) -> None:
        self.pmax = self.df_opt['POINT'].max() + self.prange + 1
        self.pmin = self.df_opt['POINT'].min() - self.prange
        
        self.df_cal = pd.DataFrame(index = range(self.pmin, self.pmax, 1))
        
        # Cal option
        for i in range(len(self.df_opt)):
            opttypecur = self.df_opt.loc[i, 'OPTTYPE']
            pointcur = self.df_opt.loc[i, 'POINT']
            unitcur = self.df_opt.loc[i, 'UNIT']
            costcur = float(self.df_opt.loc[i, 'COST'])
            addcol = str(i)+opttypecur+str(pointcur)+'-'+str(unitcur)
            self.df_cal[addcol] =  [i for i in range(self.pmin, self.pmax, 1)]
            if opttypecur == 'BC':
                self.df_cal[addcol] = (self.df_cal[addcol].apply(lambda p: -costcur if p <= pointcur else p - pointcur - costcur)) * unitcur
            elif opttypecur == 'BP':
                self.df_cal[addcol] = (self.df_cal[addcol].apply(lambda p: -costcur if p >= pointcur else pointcur - p - costcur)) * unitcur
            elif opttypecur == 'SC':
                self.df_cal[addcol] = (self.df_cal[addcol].apply(lambda p: costcur if p <= pointcur else pointcur - p + costcur)) * unitcur
            elif opttypecur == 'SP':
                self.df_cal[addcol] = (self.df_cal[addcol].apply(lambda p: costcur if p >= pointcur else p - pointcur + costcur)) * unitcur

    #show layout & revenue   
    def show(self):
        fig = plt.figure(figsize=(12,8), tight_layout=True)
        fig.suptitle('OPTION Layout and Revenue', fontsize=16)
        
        ax1 = fig.add_subplot(6, 2, (1,6))
        ax2 = fig.add_subplot(6, 2, (7,10))
        ax3 = fig.add_subplot(6, 2, 11)
        
        colors = self.df_opt['OPTTYPE'].apply(lambda s:'g' if s[0:1]=='B' else 'r').to_list()
        self.df_cal.plot(color=colors, grid = True, ax=ax1)
        
        ax1.xaxis.set_tick_params(rotation=45)
        x_major_locator=MultipleLocator(50)
        ax1.xaxis.set_major_locator(x_major_locator)
        ax1.set_title('LAYOUT')
        ax1.legend(loc=1)
        ax1.set_xlim(self.pmin, self.pmax)
        ax1.axhline(y=0, color='black', linewidth=2)
        
        
        self.df_cal.sum(axis=1).plot(ax=ax2)
        ax2.xaxis.set_tick_params(rotation=45)
        ax2.xaxis.set_major_locator(x_major_locator)
        ax2.set_title(f'REVENUE ( {self.df_cal.sum(axis=1).min()} ~ {self.df_cal.sum(axis=1).max()} )')
        ax2.set_xlim(self.pmin, self.pmax)
        ax2.axhline(y=0, color='black', linewidth=2)
        ax2.grid() 
        
        df_temp = self.df_opt[['OPTTYPE','UNIT']]
        df_temp = df_temp.groupby('OPTTYPE').sum()
        ax3.bar(df_temp.index , df_temp['UNIT'])
        ax3.grid() 
        plt.tight_layout()
        # plt.show() 
        return fig