<template>
    <window :content="winTip" ref="winTipWindow"/>
    <window :content="tip" ref="tipWindow"/>
    <div class="GameView">
        <div class = "IndexBoardContainer">
            <board :isAITurn="isAITurn" :pieces="pieces" :isEnd="isEnd"  @click-message="handleClickMessage" :hasStarted="hasStarted" ref="boardRef"/>
            <div class = "showFetch">
                <div class = "selectModel">
                    <label for="dropdown">选择模型</label>
                    <select id="dropdown" v-model="selectedModel">
                        <option v-for="option in options" :key="option.value" :value="option.value">
                            {{ option.text }}
                        </option>
                    </select>
                </div>
                <div class = "showAIFetch">
                    <img src = "@/assets/robot.png">
                    <img :src = "robotFetchPngSrc">
                    <p v-show="isAITurn">思考中...</p>
                </div>
                <div class = "showPlayerFetch">
                    <img src = "@/assets/player.png">
                    <img :src = "playerFetchPngSrc">
                </div>
            </div>
        </div>
        <div class="buttons d-flex justify-content-center mt-3">
            <el-button class="btn btn-primary mx-2" @click="handleStart" :disabled="hasStarted">开始</el-button>
            <el-button class="btn btn-secondary mx-2" @click="handleBackMove" :disabled="isAITurn || !backPieceAble || isEnd">悔一步棋</el-button>
            <el-button class="btn btn-success mx-2" @click="handleClickRank">编号</el-button>
            <el-button class="btn btn-warning mx-2" @click="handleRestartClick" :disabled="isAITurn || !hasStarted">重新开始</el-button>
            <el-button class="btn btn-info mx-2" @click="handleAITip" :disabled="isAITurn || !hasStarted || isEnd">提示</el-button>
            <el-button class="btn btn-danger mx-2" @click="handleFlipFetch" :disabled="hasStarted">更换执子</el-button>
        </div>
    </div>
</template>

<script>
import board from "../components/board.vue";
import window from "../components/window.vue"
import api from "../api/http.js";
import {ElButton, ElDialog, ElImage, ElStep} from 'element-plus';
import whitePiece from '@/assets/whitePiece.png';
import blackPiece from '@/assets/blackPiece.png';
import { ElMessage } from "element-plus";
//import {useStore} from 'vuex';

function lineToCoordinate(index,boardSize){
  const coorX = index % boardSize;
  const coorY = boardSize - Math.floor(index/boardSize) - 1;
  return [coorX,coorY];
}

function coorXYToStandard(x,y,boardSize){
    const x_coordinate = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O']
    const coorX = x_coordinate[x];
    const coorY = (boardSize-y).toString();
    return coorX+coorY;
}

export default{
    props: ['id'],
    components:{
        board,
        ElButton,
        ElImage,
        ElDialog,
        window,
    },
    data:function(){
        return{
            isAITurn :false,
            pieces:[],
            fetch:1,  //执子: 1代表先手  2代表后手
            hasStarted:false,
            tip:"z-1",
            board:[],
            boardSize:15,
            isEnd: false,
            endLine:[],
            winner: 0,
            selectedModel:"5000",
            options:[
                {value:'5000',text:'5000'},
                {value:'3000',text:'3000'},
                {value:'2000',text:'2000'},
                {value:'1000',text:'1000'}
            ],
            //store : useStore()
        }
    },
    methods:{
        handleClickMessage(index){
            //console.log("received line:",index);
            this.isAITurn = true;
            this.pieces.push(index);
            let coorXY = lineToCoordinate(index,this.boardSize);
            this.board[coorXY[1]][coorXY[0]] = this.fetch;
            if (this.checkIsEnd(coorXY[1],coorXY[0])){
                this.$refs.winTipWindow.openModal();
                this.$refs.boardRef.drawEndLine(this.endLine[0],this.endLine[1],this.fetch);
            }
            let pos = -1;

            if(this.selectedModel=="3000")
                pos = this.getNextMove();
            else if(this.selectedModel=="2000")
                pos = this.getLowNextMove();
            else if(this.selectedModel=="1000")
                pos = this.getBadNextMove();
            else if(this.selectedModel=="5000")
                pos = this.getBestNextMove();
            pos.then((movePos)=>{
                console.log("next step",movePos);
                this.pieces.push(movePos);
                coorXY = lineToCoordinate(movePos,this.boardSize);
                this.board[coorXY[1]][coorXY[0]] = 3 - this.fetch;
                this.$refs.boardRef.drawLastPiece();
                if (this.checkIsEnd(coorXY[1],coorXY[0])){
                    this.$refs.winTipWindow.openModal();
                    this.$refs.boardRef.drawEndLine(this.endLine[0],this.endLine[1],3-this.fetch);
                }
                this.isAITurn = false;
                //console.log(this.board);
            }).catch((error)=>{
                console.error('Error:',error);
            })
        },
        async getNextMove() {
            try {
                const response = await api.service.post('/chess/next_step', {
                    chess: this.pieces,
                });
                return response.data.pos;
            } catch (error) {
                console.error('Error:', error);
                throw error; // 抛出错误，以便在外部捕获
            }
        },
        async getLowNextMove() {
            try {
                const response = await api.service.post('/chess/next_step_low', {
                    chess: this.pieces,
                });
                return response.data.pos;
            } catch (error) {
                console.error('Error:', error);
                throw error; // 抛出错误，以便在外部捕获
            }
        },
        async getBadNextMove() {
            try {
                const response = await api.service.post('/chess/next_step_bad', {
                    chess: this.pieces,
                });
                return response.data.pos;
            } catch (error) {
                console.error('Error:', error);
                throw error; // 抛出错误，以便在外部捕获
            }
        },
        async getBestNextMove(){
            try{
                const response = await api.service.post('/chess/next_step_best',{
                    chess: this.pieces,
                });
                return response.data.pos;
            }catch(error){
                console.log('Error:',error);
                throw error;
            }
        },
        handleBackMove(){
            if(this.fetch == 2){
                if(this.pieces.length ==1){
                    return;
                }
            }
            let movePos = this.pieces.pop();
            let coorXY = lineToCoordinate(movePos,this.boardSize);
            this.board[coorXY[1]][coorXY[0]] = 0;
            movePos = this.pieces.pop();
            coorXY = lineToCoordinate(movePos,this.boardSize);
            this.board[coorXY[1]][coorXY[0]] = 0;
            this.$refs.boardRef.reDrawPiecesLayer();
        },
        handleClickRank(){
            this.$store.commit('flipShowIndex');
            console.log("store.state.showIndex",this.$store.state.showIndex);
            this.$refs.boardRef.reDrawPiecesLayer();
            if(this.isEnd){
                this.$refs.boardRef.drawEndLine(this.endLine[0],this.endLine[1],this.winner);
            }
        },
        handleRestartClick(){
            this.pieces.length = 0;
            this.resetBoard();
            this.winner = 0;
            this.isEnd = false;
            this.isAITurn = false;
            this.endLine=[];
            this.$refs.boardRef.reDrawPiecesLayer();
            console.log("重新开始游戏");
            this.hasStarted = false;
        },
        handleAITip(){
            this.isAITurn = true;
            const pos = this.getNextMove();
            pos.then((movePos)=>{
                console.log("获得提示:",movePos);
                let coorXY = lineToCoordinate(movePos,this.$refs.boardRef.boardSize);
                let x = coorXY[0];
                let y = coorXY[1];
                this.tip=coorXYToStandard(x,y,this.$refs.boardRef.boardSize);
                this.$refs.tipWindow.openModal();
                this.isAITurn = false;
            }).catch((error)=>{
                console.error('Error:',error);
            })
        },
        handleFlipFetch(){
            this.fetch = 3 - this.fetch;
        },
        handleStart(){
            this.hasStarted = true;
            this.resetBoard();
            console.log("开始游戏");
            if(this.fetch==1){
                return
            }
            else{
                this.isAITurn = true;
                const pos = this.getNextMove();
                pos.then((movePos)=>{
                console.log("next step",movePos);
                this.pieces.push(movePos);
                const coorXY = lineToCoordinate(movePos,this.boardSize);
                this.board[coorXY[1]][coorXY[0]] = 3 - this.fetch;
                this.$refs.boardRef.drawLastPiece();
                this.isAITurn = false;
                }).catch((error)=>{
                    console.error('Error:',error);
                })
            }
        },
        checkIsEnd(x,y){
            const directions = [[1,0],[0,1],[1,1],[1,-1]];
            for(let index = 0; index<=3; index++){
                if(this.checkOneDirection(x,y,directions[index][0],directions[index][1]))
                    return true;
            }
            return false;
        },
        checkOneDirection(x,y,dx,dy){
            const currentPiece = this.board[x][y];
            let connectedNum = 0;

            for(let index=-4; index<=4; index++){
                if(x+index*dx<0||x+index*dx>14||y+index*dy<0||y+index*dy>14)
                    continue;
                if(this.board[x+index*dx][y+index*dy] == currentPiece){
                    connectedNum += 1;
                    //console.log("player:"+this.board[x][y]+"  "+"connectedNum:"+connectedNum)
                    if(connectedNum == 5){
                        let pos = [];
                        pos.push(x+index*dx);
                        pos.push(y+index*dy);
                        this.endLine.push(pos);
                        pos=[];
                        pos.push(x+(index-4)*dx);
                        pos.push(y+(index-4)*dy);
                        this.endLine.push(pos);
                        this.winner = this.board[x][y];
                        this.isEnd = true;
                        console.log("结束了"+this.endLine)
                        return true;
                    }
                }
                else{
                    connectedNum = 0;
                }
            }
            return false;
        },
        resetBoard(){
            for(let i=0;i<this.boardSize;i++){
                this.board[i] = [];
                for(let j=0;j<this.boardSize;j++){
                    this.board[i][j] = 0;
                }
            }
        }
    },
    computed:{
        backPieceAble(){
            return (this.fetch==2 && this.pieces.length >1) || (this.fetch==1&&this.pieces.length>0);
        },
        robotFetchPngSrc(){
            return this.fetch==1? whitePiece:blackPiece;
        },
        playerFetchPngSrc(){
            return this.fetch==1? blackPiece:whitePiece;
        },
        winTip(){
            const winner = this.fetch == this.winner ? "玩家":"AI" ;
            const winTip = winner+"获胜";
            return winTip;
        }
    }
}

</script>

<style scoped>

.GameView{
  display:flex;
  flex-direction: column; /*垂直子元素排列 */
  background-image: url('@/assets/woodfloor.jpg'); 
  background-size: cover;  /* 背景图片覆盖整个元素 */
  background-position: center;  /* 背景图片居中 */
  background-size: contain;  /* 背景图片完全可见 */
  background-repeat: repeat-x;  /* 水平方向重复图片 */
  height: 100vh;  /* 设置高度为视口高度 */
}

.IndexBoardContainer{
    display: flex;
    align-items: center;  /*垂直居中对齐*/ 
    justify-content: space-between;  /*水平间距*/
    height: 100vh;
    padding: 20px;  /*内边距*/ 
}

.showFetch{
    display: flex;
    flex-direction: column; /*垂直子元素排列 */
    gap:10px; /*子元素间距 */
    margin-right: 300px;
}

.showAIFetch, .showPlayerFetch {
  display: flex;
  align-items: center; /* 垂直居中对齐 */
  gap: 10px; /* 图像之间的间距 */
}

.showAIFetch img, .showPlayerFetch img {
  max-width: 50px; /* 图像的最大宽度 */
  max-height: 50px; /* 图像的最大高度 */
  object-fit: cover; /* 保持图像的宽高比 */
}

.buttons {
  width: 100%; /* 使按钮容器占据整个宽度 */
}

.btn {
  flex: 1; /* 使每个按钮占据相等的空间 */
  min-width: 100px; /* 最小宽度 */
}

.btn:disabled, .btn[disabled] {
  opacity: 0.5; /* 降低透明度 */
  background-color: #cccccc; /* 改变背景颜色 */
  border-color: #cccccc; /* 改变边框颜色 */
  color: #666666; /* 改变文字颜色 */
  cursor: not-allowed; /* 改变鼠标指针样式 */
}

p {
  position: absolute;
  margin-left: 130px;
  margin-top: 10px;
  padding: 5px 0;
  font-size: large;
  font-family: 'KaiTi', '楷体_GB2312', serif; /* 设置为楷体 */
  color:aqua;
}

select {
  padding: 8px;
  margin-top: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
</style>
