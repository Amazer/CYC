### NGUI层级中间的特效显示

##### 1.使用NGUI的过程中，有一个具有**半透明**效果的特效，想显示在Panel_A和Panel_B中间。

        效果如下图所示：
        
  - 实现原理:
  
    - UIPanel下的界面渲染顺序，由UIDrawCall.renderQueue决定。
        >最终，使用Material.renderQueue=x来设定渲染顺序
         打开UIPanel下的"Show Draw Calls",可以看到每个Widget的渲染序列 RenderQ的值。
         想要把特效显示在界面中间，只要改变特效的渲染序列就可以了
         因此,我们可以先获取到特效的Materials,修改每一个材质的renderQueue，代码如下：

         ```c#
        using UnityEngine;
        using System.Collections;

        public class Shaderutility {
            public static void ChangeQueue(GameObject go,int queue)
            {
                if(go==null)
                {
                    return;
                }
                Renderer[] re = go.GetComponentsInChildren<Renderer>();
                if(re==null)
                {
                    return;
                }

                for(int i=0,imax=re.Length;i<imax;++i)
                {
                    for(int k=0,kmax=re[i].materials.Length;k<kmax;++k)
                    {
                        re[i].materials[k].renderQueue = queue;
                    }
                }
            }
        }
         ```
    
##### 2.有一个展示模型，在Panel_A中,当打开Panel_B的时候，希望能遮挡住模型
            效果如下图所示：

  - 实现原理:
      - 不透明的物体，可以通过z轴区分在前在后。
          >因此，只需要让模型的z在Panel_A和Panel_B中间即可。



##### 3.深入理解Shader的渲染
 - ZTest、ZWrite   
 - AlphaTest、Blend
 - 渲染顺序


