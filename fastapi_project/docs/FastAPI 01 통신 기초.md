---
title: 📄 [FastAPI] 01 통신 기초
category:
  - PYTHON
date: 2025-03-08 19:08
tags:
  - "#통신"
  - "#FastAPI"
---
![](https://www.dropbox.com/scl/fi/gcpzyxxk66ro3qeylc7h4/thumbnail_fastapi.png?rlkey=nes5rkrzls0w3ct79rqvnmy66&st=57dyseyn&dl=1)

## 1. 클라이언트와 서버

<div align="center">
<img src="https://www.dropbox.com/scl/fi/pi2ljr4pavnv4ubprwv7c/001.png?rlkey=c06jkdihij1cvbqjy0akz1yd1&dl=1" width="80%">
</div>

* 클라이언트(Client) : 데이터를 요청하는 역할. ex. 브라우저(크롬, 엣지 등)
* REST API: 클라이언트의 요청을 서버에 전달하고, 서버의 응답을 클라이언트에 반환하는 역할
* 서버(Server) : 요청을 받아 처리한 후, 응답을 보내는 역할

## 2. HTTP 통신
### 1) HTTP(HyperText Transfer Protocol)

* 클라이언트와 서버 사이에서 정보를 교환하는 규칙
* 요청(Response)과 응답(Response)으로 구성된다.
* TCP/IP[[ ]]네트워크 위에서 동작한다.

### 2) HTTP 메서드

<table>
	<thead>
		<th>Method</th>
		<th>설명</th>
		<th>예시</th>
	</thead>
	<tbody>
		<tr>
			<td>GET</td>
			<td>데이터를 <b>조회</b>할 때 사용</td>
			<td>GET /users</td>
		</tr>
		<tr>
			<td>POST</td>
			<td>데이터를 <b>생성</b>할 때 사용</td>
			<td>POST /users</td>
		</tr>
		<tr>
			<td>PUT</td>
			<td>데이터를 <b>수정</b>할 때 사용</td>
			<td>PUT /users/{user_id}</td>
		</tr>
		<tr>
			<td>PATCH</td>
			<td>데이터를 수정할 때 사용<b>(부분 수정)</b></td>
			<td>PATCH /user/{user_id}</td>
		</tr>
		<tr>
			<td>DELETE</td>
			<td>데이터를 <b>삭제</b>할 때 사용</td>
			<td>DELETE /users/{user_id}</td>
		</tr>
	</tbody>
</table>

#### 📌 PUT과 PATCH의 차이

간단히 설명하면 PUT은 덮어쓰기 PATCH는 업데이트라고 생각하면 된다. 

user의 정보가 다음과 같다고 하자. 

```
{
	'id': 1
	'name': 'Hong Gil-dong',
	'age': 20
}
```

그리고 업데이트할 데이터를 다음과 같다고 하자. 이 때 결과의 차이는 아래 표와 같다.

```
{
	'name': 'Hong Gil-Dong'
	'email': 'gildong@example.com'
}
```

<table width="100%">
	<th>PUT 요청 결과</th>
	<th>PATCH 요청 결과</th>
	<tr>
		<td> 
			<pre><code>
{
	'id': 1
	'name': 'Hong Gil-Dong',
	'email': 'gildong@example.com'
}
			</code></pre>
		</td>
		<td>
			<pre><code>
{
	'id': 1
	'name': 'Hong Gil-Dong',
	'age': 20,
	'email': 'gildong@example.com'
}
			</code></pre>
		</td>
	</tr>
</table>

## 3. REST API

### 1) REST(REpresentational State Transfer)

* 클라이언트와 서버 사이에 데이터를 주고받는 원칙
* 데이터를 **자원(Resource)** 이라고 할 때 자원을 URL로 식별하고, HTTP 메서드를 사용하여 통신
* 이때 자원은 **명사** 로 표현한다. 

### 2) REST API

* REST에 따라 설계된 API
* 클라이언트는 서버에 요청할 때 REST API만 호출하면 된다.
* 서버는 요청을 받을 때마다 독립적으로 처리한다.(Stateless)
* 데이터를 JSON 형식으로 주고 받는다.

<table>
	<thead><th>요청 내용</th><th>Method</th><th>URL</th></thead>
	<tbody>
		<tr>
			<td>전체 상품 조회</td>
			<td>GET</td>
			<td>/items</td>
		</tr>
		<tr>
			<td>특정 상품 조회</td>
			<td>GET</td>
			<td>/items/{item_id}</td>
		</tr>
		<tr>
			<td>새로운 상품 추가</td>
			<td>POST</td>
			<td>/items</td>
		</tr>
		<tr>
			<td>특정 상품 수정(전체 업데이트)</td>
			<td>PUT</td>
			<td>/items/{item_id}</td>
		</tr>
		<tr>
			<td>특정 상품 수정(부분 업데이트)</td>
			<td>PATCH</td>
			<td>/items/{item_id}</td>
		</tr>
		 <tr>
			<td>특정 상품 삭제</td>
			<td>DELETE</td>
			<td>/items/{item_id}</td>
		</tr>
	</tbody>	
</table>

### 3) RESTful API

* REST를 잘 지킨 API를 RESTful API라고 한다. 
* RESTful API에서는 일반적으로 URL에 동사를 사용하지 않지만, 예외적으로 동사를 사용할 수도 있다. (ex. 로그인: POST /login)
* 자원을 식별할 때는 보통 URL 경로(Path Parameter)를 사용하며, ID 같은 주요 식별자를 쿼리문(Query Parameter)로 받는 것은 권장되지 않는다.
* 쿼리문(Query Parameter)은 필터, 검색, 정렬, 페이지네이션 등에 사용된다.

## 3. Socket 통신

### 1) 패킷(Packet)

* 데이터를 보내는 작은 조각
* 인터넷으로 데이터를 전송할 때에는 데이터의 구초를 해체한 후 여러 개의 패킷(packet)으로 쪼개 전송한다. 
### 2) TCP와 UDP

#### TCP(Transmission Control Protocol)

* 전송 제어 프로토콜이라고 한다. 
* 데이터가 손실되지 않도록 패킷을 순서대로 보내고, 도착 여부를 확인한다

#### UDP(User Datagram Protocal)

* 사용자 데이터그램 프로토콜이라고 한다. 
* 데이터가 손실될 수 있지만, 빠르게 보내는 것이 중요할 때 사용한다. 

### 3) TCP vs UDP 비교표

<table width="100%">
	<thead>
		<th width="20%">구분</th>
		<th>TCP</th>
		<th>UDP</th>
	</thead>
	<tbody>
		<tr>
			<td>데이터 전송 방식</td>
			<td>연결을 확인하고 순서대로 전송</td>
			<td>순서를 보장하지 않고 전송</td>
		</tr>
		<tr>
			<td>속도</td>
			<td>연결을 확인해야하기 때문에 느림</td>
			<td>연결 확인이 필요없어 빠름</td>
		</tr>
		<tr>
			<td>신뢰성</td>
			<td>높음(패킷 손실 시 재전송)</td>
			<td>낮음(패킷 손실)</td>
		</tr>
		<tr>
			<td>예시</td>
			<td>HTTP, SMTP, FTP</td>
			<td>실시간 영상 스트리밍</td>
		</tr>
	</tbody>
</table>
