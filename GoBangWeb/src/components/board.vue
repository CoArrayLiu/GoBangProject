<template>
  <div class = board>
    <div class = "board-canvas-container">
      <canvas id="board" ref="canvasboard" :width="boardwidth" :height="boardheight"></canvas>
      <canvas id="piece" ref="canvaspiece" :width="boardwidth" :height="boardheight"></canvas>
      <canvas 
        id="realtime" 
        ref="canvasrealtime" 
        :width="boardwidth" 
        :height="boardheight"
        @contextmenu.prevent
        @mousedown="onMouseDown"
        @touchstart="onMouseDown"
      ></canvas>
    </div>
  </div>


</template>

<script>
function drawBoardBackground(ctx,ratio,width,height){
  const startX = 0 + (width - width*ratio)/2;
  const startY = 0 + (height - height*ratio)/2;
  ctx.beginPath();
  ctx.rect(startX,startY,width*ratio,height*ratio);
  ctx.fillStyle = '#DAA520';
  ctx.fill();
}

function drawLines(ctx,ratio,width,height,boardSize,borderLineWidth,lineWidth){
  const startX = 0 + (width - width*ratio)/2;
  const startY = 0 + (height - height*ratio)/2;
  const widthLineInterval = width*ratio/(boardSize-1);
  const heightLineInterval = height*ratio/(boardSize-1);
  ctx.strokeStyle = 'black';
  //画横线
  for(let x = startX; x <= width-startX ; x += heightLineInterval){
    if(Math.abs(x - startX)<=2 || Math.abs(x - width+startX)<=2){
      ctx.lineWidth = borderLineWidth;
    }
    else{
      ctx.lineWidth = lineWidth;
    }
    ctx.beginPath();
    ctx.moveTo(x,startY);
    ctx.lineTo(x,width-startX);
    ctx.stroke();
  }
  //画竖线
  for(let y = startY; y <= height-startY ; y+= widthLineInterval){
    if(Math.abs(y - startY)<=2 || Math.abs(y - height+startY)<=2){
      ctx.lineWidth = borderLineWidth;
    }
    else{
      ctx.lineWidth = lineWidth;
    }
    ctx.beginPath();
    ctx.moveTo(startX,y);
    ctx.lineTo(height-startY,y);
    ctx.stroke();
  }

}

function drawCoordinateText(ctx,rectRatio,boardRatio,width,height,boardSize){
  const x_coordinate = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O']

  ctx.font = '20px "楷体", "Microsoft YaHei", sans-serif';
  ctx.fillStyle = 'black';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';

  const widthLineInterval = width*boardRatio/(boardSize-1);
  const heightLineInterval = height*boardRatio/(boardSize-1);

  //横坐标
  let startX = 0 + (width - width*boardRatio)/2;
  let Y = height - (height - height*rectRatio)/4;
  let endX = width - startX;
  let index = 0;
  for(let x = startX; x <= endX; x += widthLineInterval){
    ctx.fillText(x_coordinate[index],x,Y);
    index += 1;
  }
  //纵坐标
  index = 0;
  let X = (width - width*rectRatio)/4;
  let startY = height - (height - height*boardRatio)/2;
  let endY = 0;
  for(let y = startY;y >= endY; y -= heightLineInterval){
    if(index>=boardSize)
      break
    index += 1;
    ctx.fillText(index,X,y);
  }
  index = 0;
  X = width - (width - width*rectRatio)/4;
  for(let y = startY;y >= endY; y -= heightLineInterval){
    if(index>=boardSize)
      break
    index += 1;
    ctx.fillText(index,X,y);
  }
}

function drawTagDot(ctx,ratio,width,height,boardSize,radius){
  const startX = 0 + (width - width*ratio)/2;
  const startY = 0 + (height - height*ratio)/2;
  const widthLineInterval = width*ratio/(boardSize-1);
  const heightLineInterval = height*ratio/(boardSize-1);

  let x = startX + 3*widthLineInterval;
  let y = startY + 3*heightLineInterval;
  drawCircle(ctx,x,y,radius,'black');
  x = startX + 11*widthLineInterval;
  y = startY + 11*heightLineInterval;
  drawCircle(ctx,x,y,radius,'black');
  x = startX + 3*widthLineInterval;
  y = startY + 11*heightLineInterval;
  drawCircle(ctx,x,y,radius,'black');
  x = startX + 11*widthLineInterval;
  y = startY + 3*heightLineInterval;
  drawCircle(ctx,x,y,radius,'black');
  x = startX + 7*widthLineInterval;
  y = startY + 7*heightLineInterval;
  drawCircle(ctx,x,y,radius,'black');
}

function drawCircle(ctx,x,y,radius,color,lineWidth = 1){
  ctx.beginPath();
  ctx.arc(x,y,radius,0,Math.PI*2);
  ctx.strokeStyle = 'black';
  ctx.fillStyle = color;
  ctx.lineWidth = lineWidth;
  ctx.fill();
  ctx.stroke();
}

function screenXYToCoordinate(width,height,screenX,screenY,boardRatio,boardSize){
  const widthBorder = width*(1-boardRatio)/2;
  const heightBorder = height*(1-boardRatio)/2;
  const widthInterval = width*boardRatio/(boardSize-1);
  const heightInterval = height*boardRatio/(boardSize-1);
  
  let x = (screenX - widthBorder)/widthInterval ;
  let y = (screenY - heightBorder)/heightInterval ;
  //console.log(x,y);
  x = Math.round(x);
  y = Math.round(y);

  return [x,y];
}

function coordinateToCircleCenter(width,height,coorX,coorY,boardRatio,boardSize){
  const widthBorder = width*(1-boardRatio)/2;
  const heightBorder = height*(1-boardRatio)/2;
  const widthInterval = width*boardRatio/(boardSize-1);
  const heightInterval = height*boardRatio/(boardSize-1);

  const screenX = widthBorder + coorX*widthInterval;
  const screenY = heightBorder + coorY*heightInterval;

  return [screenX,screenY]
}

function drawText(ctx,x,y,text,font_size,color='black'){
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.font = Math.floor(font_size).toString()+'px Arial';
  ctx.fillStyle = color; // 字体颜色
  ctx.fillText(text,x,y);
}

function drawPiece(ctx,width,height,coorX,coorY,boardRatio,color,boardSize=15,showIndex,text=null){
  const screenXY = coordinateToCircleCenter(width,height,coorX,coorY,boardRatio,boardSize);
  const screenX = screenXY[0];
  const screenY = screenXY[1];
  const radius = width*boardRatio/(boardSize-1)/2.05;

  drawCircle(ctx,screenX,screenY,radius,color);

  if(showIndex && text){
    let font_color = (color == 'black'? 'white':'black');
    drawText(ctx,screenX,screenY,text,radius,font_color);
  }
}

function coordinateToLine(coorX,coorY,boardSize){
  const index = coorX + (boardSize - coorY -1)*boardSize;
  return index;
}

function lineToCoordinate(index,boardSize){
  const coorX = index % boardSize;
  const coorY = boardSize - Math.floor(index/boardSize) - 1;
  return [coorX,coorY];
}

function reDrawPieces(pieces,ctx,width,height,boardRatio,boardSize,showIndex){
  ctx.clearRect(0,0,width,height);
  let coorXY = [-1,-1];
  let coorX = -1;
  let coorY = -1;
  let color = 'orange';
  pieces.forEach(function(piece,index){
    coorXY = lineToCoordinate(piece,boardSize);
    coorX = coorXY[0];
    coorY = coorXY[1];
    color = index%2==0 ? 'black':'white';
    const posInList = index + 1;
    drawPiece(ctx,width,height,coorX,coorY,boardRatio,color,boardSize,showIndex,posInList.toString());
  })
}

function toDrawEndLine(ctx,width,height,boardRatio,boardSize,start,end,lineWidth,lineColor='red'){
  const startXY = coordinateToCircleCenter(width,height,start[0],start[1],boardRatio,boardSize);
  const endXY = coordinateToCircleCenter(width,height,end[0],end[1],boardRatio,boardSize);
  ctx.lineWidth = lineWidth;
  ctx.strokeStyle=lineColor;
  ctx.beginPath();
  ctx.moveTo(startXY[1],startXY[0]);
  ctx.lineTo(endXY[1],endXY[0]);
  ctx.stroke();
}

export default{
  props:{
    isAITurn:Boolean,
    pieces:{
      type:Array,
      Required:true,
    },
    hasStarted:Boolean,
    isEnd:Boolean,
  },
  data: function(){
    return{
      boardSize : 15,
      boardwidth : 550,
      boardheight : 550,
      rectRatio:0.93,
      boardRatio:0.86,
      boardBorderLineWidth:3,
      boardLineWidth:1,
      tagDotRadius:4,
      endLineWidth:5,

    }
  },
  mounted(){
    this.ctx = this.context('board');
    this.initDrawingContext()
  },
  methods:{
    initDrawingContext(){
      drawBoardBackground(this.ctx,this.rectRatio,this.boardwidth,this.boardheight);
      drawLines(this.ctx,this.boardRatio,this.boardwidth,this.boardheight,this.boardSize,this.boardBorderLineWidth,this.boardLineWidth);
      drawCoordinateText(this.ctx,this.rectRatio,this.boardRatio,this.boardwidth,this.boardheight,this.boardSize);
      drawTagDot(this.ctx,this.boardRatio,this.boardwidth,this.boardheight,this.boardSize,this.tagDotRadius)
    },
    onMouseDown(event){
      //console.log("click event")
      //console.log("isAITurn:"+this.isAITurn)

      const canvasRect = this.$refs.canvasrealtime.getBoundingClientRect();
      const offsetX = event.clientX - canvasRect.left;
      const offsetY = event.clientY - canvasRect.top;

      let coordinate = screenXYToCoordinate(this.boardwidth,this.boardheight,offsetX,offsetY,this.boardRatio,this.boardSize);
      let x = coordinate[0];
      let y = coordinate[1];
      let index = coordinateToLine(x,y,this.boardSize);

      if(x<0 || x>14 || y<0 || y>14 || this.pieces.includes(index) || this.isAITurn || !this.hasStarted || this.isEnd){
        return;
      }

      console.log(x,y,index);
      
      let color = this.pieces.length%2 == 0 ? 'black':'white';
      const posInlist = this.pieces.length +1;
      drawPiece(this.context('piece'),this.boardwidth,this.boardheight,x,y,this.boardRatio,color,this.boardSize,this.$store.state.showIndex,posInlist.toString());
      
      this.$emit('click-message',index);
    },
    reDrawPiecesLayer(){
      console.log("重画棋子图层");
      reDrawPieces(this.pieces,this.context('piece'),this.boardwidth,this.boardheight,this.boardRatio,this.boardSize,this.$store.state.showIndex);
    },
    drawLastPiece(){
      const coorXY = lineToCoordinate(this.pieces.at(-1),this.boardSize);
      const x = coorXY[0];
      const y = coorXY[1];
      let color = this.pieces.length%2 == 1 ? 'black':'white';
      let posInList = this.pieces.length;
      drawPiece(this.context('piece'),this.boardwidth,this.boardheight,x,y,this.boardRatio,color,this.boardSize,this.$store.state.showIndex,posInList.toString());
    },
    drawEndLine(start,end,player){
      let color = player==1? 'white':'black';
      //其他可选颜色:
      //#4A86E8  较深的明亮蓝色
      //#4682B4  钢蓝
      //#6495ED  深天蓝
      //#87CEFA  浅蓝色
      //#FF851B  橙色
      //#3F51B5  候选蓝
      //#FFDC00  黄色
      //#2ECC40  绿色
      color = "#2ECC40";  //绿色
      toDrawEndLine(this.context('piece'),this.boardwidth,this.boardheight,this.boardRatio,this.boardSize,start,end,this.endLineWidth,color);
    }
  },
  computed:{
    context(){
      return (idx) => {
        return this.$refs['canvas'+idx].getContext('2d')
      }
    }
  }
}

</script>


<style scoped>
.board {
  width: 100%;
}
.board-canvas-container {
  position: relative;
  margin: 0 auto;
  width: 550px; 
  height: 550px; 
}

canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  touch-action: none; /* 确保触摸事件传递给底层元素 */
}

#board {
  z-index: 1;
}

#piece {
  z-index: 2;
}

#realtime {
  z-index: 3;
}
</style>
