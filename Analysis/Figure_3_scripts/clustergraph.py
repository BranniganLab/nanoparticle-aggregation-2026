import glob
import matplotlib.pyplot as plt
import numpy as np
import random
from pathlib import Path

FilePath = Path.cwd()

def GrabFiles():
    """
    Gets files with that begin with Cluster and end with .dat

    Returns
    -------
    Objectcontainer : list
        returns a list of parse objects.

    """
    Objectcontainer = []
    filelist = glob.glob("Cluster*.dat")
    assert filelist != [], f"Cluster data file doesn't exist in '{FilePath}' Directory"
    for file in filelist:
        Parseobject = NanoparticleParse(FilePath / Path(file)).ParseClusterInformation()
        Objectcontainer.append(Parseobject)
    return Objectcontainer
        
def PlotContainer(Objectcontainer,Monomer=0,LargestAggregateFraction=0):
    """
    

    Parameters
    ----------
    Objectcontainer : list
        List of objects.
    Monomer : int, optional
        Turn on or off Monomer fraction plotting with 1 or 0. The default is 0.
    LargestAggregateFraction : int, optional
        Turn on or off Largest Aggregate fraction plotting with 1 or 0. The default is 0.

    Returns
    -------
    None.

    """
    if Monomer==1:
        plotnum=1
        for obj in Objectcontainer:
            NanoparticlePlot([obj]).BasicPlot(xaxistitle="Time ($\mu s$)", yaxistitle= "Monmer Fraction", line=0.5)
            plt.savefig(FilePath / Path('Monomer'+str(plotnum)),format='pdf',dpi=500, bbox_inches='tight')
            plotnum+=1
            
    if LargestAggregateFraction==1:
        plotnum=1
        for obj in Objectcontainer:
            NanoparticlePlot([obj]).LargestAggregatePlot(xaxistitle="Time ($\mu s$)", yaxistitle= "Largest Aggregate Fraction", line=0.5)
            plt.savefig(FilePath / Path('LAF'+str(plotnum)),format='pdf',dpi=500, bbox_inches='tight')
            plotnum+=1
    

class NanoparticleParse:
    def __init__(self, ClusterFilePath):
        """
        Generates a Parsed data object

        Parameters
        ----------
        ClusterFilePath : str
            Path for cluster file.

        Returns
        -------
        None.

        """
        self.ClusterFilePath = open(ClusterFilePath)
        
    
    def ParseClusterInformation(self):
        """
        Parses Cluster script files and makes them easily plottable. 

        Returns
        -------
        list
            Returns a list of list with the frame, largest aggregate fraction and monomerfraction for each frame.

        """
        LargestAggregateFraction = []
        MonomerFraction = []
        Frame = []
        for line in self.ClusterFilePath:
            sline = line.replace("\n", "").replace(" ", "\n", 1).replace(" {{", "\n").replace("}}", "").replace(" {", "\n").replace("}", "")
            sline2 = sline.split()[1]
            if sline2.isnumeric() == True:
                sl = sline.split("\n")
            elif sline2 == "{":
                sline = sline.replace("{", "", 1).replace("}", "", 1)
                sl = sline.split("\n")
            else:
                sline = sline.replace("{", "")
                sl = sline.split("\n")
                
            Frame.append(int(sl[0])/100)
            if sl[1] == "":
                MonomerFraction.append(0)
            else:
                NumberList = self.ConvertStringListToNumList(sl[1])
                Monomers = np.count_nonzero(NumberList)
                MonomerFraction.append(Monomers)
        
            LargestAggregateFraction.append(self.ConvertAggregateData(sl[2:]))
        
        return [Frame, LargestAggregateFraction, MonomerFraction]
    
    def ConvertStringListToNumList(self, NumberString):
        """
        Converts a string of numbers into a list.

        Parameters
        ----------
        NumberString : str
            String of numbers.

        Returns
        -------
        NumList : list
            List is numbers built from string.

        """
        StringList = NumberString.split()
        NumList = [eval(i) for i in StringList]
        return NumList

    def ConvertAggregateData(self, NumberString):
        """
        Converts string of numbers into aggregation data by counting non-zeros

        Parameters
        ----------
        NumberString : str
            String of numbers.

        Returns
        -------
        TempList : list
            list of aggregate sizes.

        """
        TempList = []
        for string in NumberString:
            NumList = self.ConvertStringListToNumList(string)
            TempList.append(np.count_nonzero(NumList))
        return TempList


class NanoparticlePlot:
    def __init__(self, DataList):
        self.DataList = DataList
        
    def RandomColorGenerator(self):
        """
        Generates random Hex colors between specific values

        Returns
        -------
        TYPE str
            Hex color string.

        """
        r = lambda: random.randint(0,255)
        return '#%02X%02X%02X' % (r(),r(),r())
    
    def BasicPlot(self, xaxistitle="x-axis", yaxistitle="y-axis", colors = None, labels = None, stepsize=1,line=0, val1 = 0, val2= 2):
        """
        

        Parameters
        ----------
        xaxistitle : str, optional
            x-axis title. The default is "x-axis".
        yaxistitle : str, optional
            y-axis title. The default is "y-axis".
        colors : str, optional
            color name or hex color value. The default is None.
        labels : list, optional
            list of axis labels. The default is None.
        stepsize : int, optional
            Jumps over data at stepsize interval. The default is 1.
        line : int, optional
            draws a vline at particulat xvalue. The default is 0.
        val1 : int, optional
            Determines which column the xvalue will be. The default is 0.
        val2 : int, optional
            Determines which column the yvalue will be. The default is 2.

        Raises
        ------
        Exception
            Ra.

        Returns
        -------
        None.

        """
        if self.DataList == []: 
            raise Exception("Must Input Cluster Data First")
        
        else:
                
            if colors == None:
                tempcolor = []
                for _ in self.DataList:
                    tempcolor.append(self.RandomColorGenerator())
                colors = tempcolor
            if labels == None:
                templabel = []
                for i in range(len(self.DataList)):
                    templabel.append("data" + str(i))
                labels = templabel
            figure , axs = plt.subplots(1, figsize=(10,8))
            
            
            for i in range(len(self.DataList)):
                axs.plot(self.DataList[i][val1],self.DataList[i][val2],linestyle='solid',linewidth=3, color=colors[i], label=labels[i])
            axs.set_xlabel(xaxistitle,fontsize=20)
            axs.set_ylabel(yaxistitle,fontsize=20)
            axs.tick_params(axis='x', labelsize=15)
            axs.tick_params(axis='y', labelsize=15)
            axs.legend(loc="lower right", fontsize="10")
            if line != 0:
                plt.axvline(x = line, color = 'green', linewidth =1, label = 'axvline - full height')
       
    
    def LargestAggregatePlot(self, totalnpnum = 10, xaxistitle="x-axis", yaxistitle="y-axis", colors = None, labels = None, stepsize=1,line=0, val1=0):
        '''
        

        Parameters
        ----------
        totalnpnum : int, optional
            Number of aggregates in system. The default is 10.
        xaxistitle : str, optional
            x-axis title. The default is "x-axis".
        yaxistitle : str, optional
            y-axis title. The default is "y-axis".
        colors : str, optional
            color name or hex color value. The default is None.
        labels : list, optional
            list of axis labels. The default is None.
        stepsize : int, optional
            Jumps over data at stepsize interval. The default is 1.
        line : int, optional
            draws a vline at particulat xvalue. The default is 0.
        val1 : int, optional
            Determines which column the xvalue will be. The default is 0.
            DESCRIPTION. The default is 0.

        Returns
        -------
        None.

        '''
        for i in range(len(self.DataList)):
            templist = []
            for num in self.DataList[i][1]:
                templist.append(max(num)/totalnpnum)
            self.DataList[i][1]= templist
        self.BasicPlot(xaxistitle, yaxistitle, colors, labels, stepsize,line, val1, val2=1)
        
if __name__=="__main__":
    
    Filobj = GrabFiles()
    PlotContainer(Filobj,1,1)
    plt.show()
    
