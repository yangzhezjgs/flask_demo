<template>
    <div id="app" class="app">
        <h1 v-text='title'></h1>
        <p class='typeInput'>
            <input type="text" v-model='newText' v-on:keyup.enter='addNewlist'>
        </p>
        <ul>
            <li v-for='item in items' v-bind:class='{finished:item.isFinished}' v-on:click='toggleFinish(item)'>{{item.text}}&nbsp&nbsp&nbsp<input v-on:click="delItem(item)" type="submit" value="delete"></li>
        </ul>
    </div>
</template>

<script>
var axios = require('axios');
export default {
  name: 'app',
  data () {
    return {
      title:'todo list',
      items:[],
      newText:''
    }
  },
   methods:{
       toggleFinish:function(item){
         axios.post('/api/update',{'text':item.text,'isFinished':item.isFinished}).then(response => {
		if(response.data.ok){
                    item.isFinished=!item.isFinished;
		}})
                },
       addNewlist:function(){
         axios.post('/api/insert',{'text':this.newText,'isFinished':false})
		.then(response => {
		if(response.data.ok){
		 this.items.push({
                            text:this.newText,
                            isFinished:false
                        })
                   this.newText='';
		}
             })
	},
	delItem:function(item){
         axios.post('/api/delete',{'text':item.text,'isFinished':item.isFinished})
		.then(response => {
		if(response.data.ok){
		 var index = this.items.indexOf(item);
		if (index > -1) {this.items.splice(index, 1)};	
		}})
	}
},

   mounted(){
	axios.get('/api/get',{
	}).then(response =>this.items = response.data)}
	
	
}
</script>

<style>
        *{
            list-style: none;
            outline: none;
            border: none;
        }
        #app{
            text-align: center;
            color: #2c3e50;
        }
        .app{
            width: 90%;
            margin: 0 auto;
            padding: 5%;
            margin-top: 10px;
        }
        .app li.finished{
            text-decoration: line-through;
        }    
        .typeInput input{
            width: 50%;
            font-size: 24px;
            border: 1px solid #000;
            padding-left:5px;
        }
</style>
