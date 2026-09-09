import React, { useEffect, useState } from 'react';
import { Card, Table, Spin, Alert, Tag, Space, Button, Popconfirm } from 'antd';
import { DeleteOutlined, ReloadOutlined } from '@ant-design/icons';
import { stockApi } from '../services/api';

function History() {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await stockApi.getScanHistory(0, 100);
      setData(response || []);
    } catch (err) {
      setError('加载历史记录失败');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const columns = [
    {
      title: '股票代码',
      dataIndex: 'code',
      key: 'code',
      width: 100,
    },
    {
      title: '股票名称',
      dataIndex: 'name',
      key: 'name',
      width: 120,
    },
    {
      title: '扫描日期',
      dataIndex: 'scan_date',
      key: 'scan_date',
      width: 120,
    },
    {
      title: '技术面',
      dataIndex: 'technical_score',
      key: 'technical_score',
      width: 100,
      render: (score) => (
        <Tag color={score >= 80 ? 'green' : score >= 60 ? 'orange' : 'red'}>
          {score.toFixed(2)}
        </Tag>
      ),
    },
    {
      title: '基本面',
      dataIndex: 'fundamental_score',
      key: 'fundamental_score',
      width: 100,
      render: (score) => (
        <Tag color={score >= 80 ? 'green' : score >= 60 ? 'orange' : 'red'}>
          {score.toFixed(2)}
        </Tag>
      ),
    },
    {
      title: '资金面',
      dataIndex: 'money_flow_score',
      key: 'money_flow_score',
      width: 100,
      render: (score) => (
        <Tag color={score >= 80 ? 'green' : score >= 60 ? 'orange' : 'red'}>
          {score.toFixed(2)}
        </Tag>
      ),
    },
    {
      title: '综合评分',
      dataIndex: 'overall_score',
      key: 'overall_score',
      width: 100,
      render: (score) => (
        <Tag color={score >= 80 ? 'green' : score >= 70 ? 'blue' : 'orange'}>
          {score.toFixed(2)}
        </Tag>
      ),
    },
    {
      title: '操作',
      key: 'action',
      width: 120,
      render: (_, record) => (
        <Space>
          <a href={`/analysis/${record.code}`}>查看详情</a>
        </Space>
      ),
    },
  ];

  return (
    <div>
      <h1>历史记录</h1>
      {error && <Alert message={error} type="error" showIcon style={{ marginBottom: 16 }} />}

      <Card
        title="扫描历史"
        extra={
          <Button icon={<ReloadOutlined />} onClick={loadHistory} loading={loading}>
            刷新
          </Button>
        }
      >
        <Table
          dataSource={data}
          columns={columns}
          rowKey={(record, index) => `${record.code}-${record.scan_date}-${index}`}
          pagination={{ pageSize: 20, showSizeChanger: true }}
          loading={loading}
          scroll={{ x: 1200 }}
        />
      </Card>
    </div>
  );
}

export default History;
