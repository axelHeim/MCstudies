import unittest
import pandas as pd


from pandas_colFuncs_physicsVars import Mbc_Btag, MM2recoilSignalSide, deltaE


class TestPhysicsFuncs(unittest.TestCase):

    def test_Mbc_Btag(self):
        
        result_Mbc_df = pd.DataFrame({ 
            'px_summed_X':["0","1","-1","0.4986732397","0.1"], 
            'py_summed_X':["0","1","-1","0.4986732397","0.2"], 
            'pz_summed_X':["0","1","-1","0.4986732397","0.3"],
            'Hc_px':["0","1","-1","0.4986732397","0.4"],
            'Hc_py':["0","1","-1","0.4986732397","0.5"],
            'Hc_pz':["0","1","-1","0.4986732397","0.6"],
            }).reset_index()
        
        target_Mbc_df = pd.DataFrame({ 
            'Mbc_Btag':["5.29","3.998012006","3.998012006","5.0","5.141410312"], 
            }).reset_index()
        
        
        #target_Mbc_df = pd.merge(result_Mbc_df,target_Mbc_df, on="index")
        
        
        for key in target_Mbc_df.keys():
            target_Mbc_df[key] = target_Mbc_df[key].astype(float)
        for key in result_Mbc_df.keys():
            result_Mbc_df[key] = result_Mbc_df[key].astype(float)
        
        result_Mbc_df['Mbc_Btag'] = result_Mbc_df.apply(Mbc_Btag,axis=1)
        
        
  
        # check if results are equal for 6 digits
        result_Mbc_df['result'] = result_Mbc_df['Mbc_Btag'].round(6) == target_Mbc_df['Mbc_Btag'].round(6)
        
        """ 
        print("target_Mbc_df:")
        print(target_Mbc_df)
        
        print(result_Mbc_df['result'])
        print("result_Mbc_df:")
        print(result_Mbc_df)
         """
         
        self.assertTrue(result_Mbc_df['result'].all())    
    
    def test_mm2(self):
        
        result_MM2_df = pd.DataFrame({ 
            'CMSpx_summed_X':["0","0.1","-0.1","1","1"], 
            'CMSpy_summed_X':["0","0.1","-0.1","-1","1"], 
            'CMSpz_summed_X':["0","0.1","-0.1","-1","1"],
            'CMSE_summed_X':["0","0.5","0.6","4","5"],  
            'CMSpx_summed_Bs':["0","0.1","-0.1","-1","1"], 
            'CMSpy_summed_Bs':["0","0.1","-0.1","1","-1"], 
            'CMSpz_summed_Bs':["0","0.1","0.2","1","1"],
            'CMSE_summed_Bs':["0","0.5","0.7","3","4"], 
            'Hc_cmpx':["0","0.1","0.1","-1","1"],
            'Hc_cmpy':["0","0.1","-0.1","-1","-1"], 
            'Hc_cmpz':["0","0.1","0.3","2","-3"]  
            }).reset_index()
        
        target_MM2_df = pd.DataFrame({ 
            'mm2':["27.9841","22.6741","20.8081","-0.7559","-9.3359"], 
            }).reset_index()
        
       
        #target_Mbc_df = pd.merge(result_Mbc_df,target_Mbc_df, on="index")
        
        
        for key in target_MM2_df.keys():
            target_MM2_df[key] = target_MM2_df[key].astype(float)
        for key in result_MM2_df.keys():
            result_MM2_df[key] = result_MM2_df[key].astype(float)
        
        result_MM2_df['mm2'] = result_MM2_df.apply(MM2recoilSignalSide,axis=1)
        
        
  
        # check if results are equal for 5 digits
        result_MM2_df['result'] = result_MM2_df['mm2'].round(5) == target_MM2_df['mm2'].round(5)
        
        """ 
        print("target_MM2_df:")
        print(target_MM2_df)
        
        print(result_MM2_df['result'])
        print("result_MM2_df:")
        print(result_MM2_df)
         """
          
        self.assertTrue(result_MM2_df['result'].all())

    def test_deltaE(self):
        
        target_deltaE_df = pd.DataFrame({ 
            'deltaE':["0","-2.71","1.291988","0.29","0.148589688"]
            }).reset_index()
        
        result_deltaE_df = pd.DataFrame({ 
            'Mbc_Btag':["5.29","8","3.998012006","5.0","5.141410312"], 
            }).reset_index()
        
        
        #target_Mbc_df = pd.merge(result_Mbc_df,target_Mbc_df, on="index")
        
        
        for key in target_deltaE_df.keys():
            target_deltaE_df[key] = target_deltaE_df[key].astype(float)
        for key in result_deltaE_df.keys():
            result_deltaE_df[key] = result_deltaE_df[key].astype(float)
        
        result_deltaE_df['deltaE'] = result_deltaE_df.apply(deltaE,axis=1)
        
        
  
        # check if results are equal for 6 digits
        result_deltaE_df['result'] = result_deltaE_df['deltaE'].round(6) == target_deltaE_df['deltaE'].round(6)
        
        """ 
        print("target_deltaE_df:")
        print(target_deltaE_df)
        
        print(result_deltaE_df['result'])
        print("result_deltaE_df:")
        print(result_deltaE_df)
         """
         
        self.assertTrue(result_deltaE_df['result'].all())




if __name__ == '__main__':
    unittest.main()
