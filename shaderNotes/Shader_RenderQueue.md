### NGUI层级中间的特效显示

##### 1.使用NGUI的过程中，有一个具有**半透明**效果的特效，想显示在Panel_A和Panel_B中间。

        效果如下图所示：
![](img/test2.jpg)
        
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
<<<<<<< HEAD
 - ZTest、ZWrite   
 - AlphaTest、Blend
 - 渲染顺序


=======
=======
>>>>>>> 2a9d0012065c8b13fd65cd651b156ce8179f13cf
 - 渲染顺序(Queue)
     > shader按照Queue序列进行操作，即，先操作 queue值小的，后操作queue大的。
     > 在Unity Shader中，表现为 subShader的Tags{"Queue"="..."}。
 - ZTest
     > Unity Shader中，如果没有指定，默认是ZTest LEqual
     > 如果深度测试没有通过，会直接丢弃掉片元；否则，进入下一步，是否写入深入值
 - ZWrite   
     > 如果打开了深度写入(Unity中默认是打开的),会将片元的深度值写入深度缓冲区；
     > 如果关闭了深度写入(ZWrite Off),则不会讲片元写入深度缓冲区。
     > 之后，进行下一步,混合操作
 - Blend(混合)
     > 如果开启了混合，会进行颜色的叠加后写入颜色缓冲区；
     > 否则，会直接将颜色写入颜色缓冲区




##### 4.Queue和ZWrite的使用过程

   - ZTest   ---> 一定会进行，默认是LEqual,也就是前面的物体会遮挡后面的物体
      > ZTest如果不通过，也就是说，被前面的遮挡着，片元就不再往下进行了
      > ZTest通过的情况下，

```flow
st=>start: 开始深度测试
e=>end: 深度测试结束
compareDepth=>operation: 比较片元深度值,得到深度测试结果
isPassZTest=>condition: 是否通过了深度测试
isZWriteOn=>condition: 是否开启了深度写入
writeZDepth=>operation: 将深度值写入深度缓冲区
dropFragment=>operation: 舍弃该片元
over=>operation: 结束
st->compareDepth->isPassZTest(yes)->isZWriteOn(yes)->writeZDepth->e->e

isPassZTest(no)->dropFragment->e->e

isZWriteOn(no)->e

```

 > 是否开启了ZWrite影响了下一个物体渲染时候的深度测试是否能够通过


  - 开启混合的Shader，ZWrite开启和关闭的必要性
    > 在开启混合的状态下:
    > 如果此物体被其他物体遮挡住了,那么在深度测试的阶段就被抛弃了；因此，开启混合的物体，一般放在最上方（or 最前面）
    > 如果没有被其他物体遮挡，z本来就是在最上方的，因此，没有必要开启ZWrite。

  - 如果所有shader都是关闭ZWrite的，并且Transform.position.z都一样:
    > 因为默认的ZTest 是LEqual 小于或者等于，所以，所有片元的ZTest都会通过。
    > 那么，渲染顺序就是材质的queue的顺序。
    > 所以，此时，可以通过修改材质的queue值，来将某个shader的渲染放到两个Panel之间
 

 - 总结
    > 1.永远关注深度值，也即transform.position.z
    > 2.如果z值相同， 修改queue
    > 3.如果z值不同，ZTest会先过滤,所以调整前后位置

