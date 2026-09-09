import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Card, Row, Col, Statistic, Spin, Alert, Button, Space, Descriptions } from 'antd';
import { ArrowLeftOutlined } from '@ant-design/icons';
import { stockApi } from '../services/api';

function Analysis() {
  const { code } = useParams();
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadAnalysis();
  }, [code]);

  const loadAnalysis = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await stockApi.analyzeStock(code);
      setData(response);
    } catch (err) {
      setError('加载分析数据失败');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <Spin size="large" style={{ display: 'flex', justifyContent: 'center', padding: '50px' }} />;
  }

  if (error) {
    return <Alert message={error} type="error" showIcon />;
  }

  if (!data) {
    return <Alert message="未找到分析数据" type="warning" showIcon />;
  }

  return (
    <div>
      <Space style={{ marginBottom: 16 }}>
        <Button icon={<ArrowLeftOutlined />} onClick={() => window.history.back()}>
          返回
        </Button>
        <h1>{data.name} ({data.code})</h1>
      </Space>

      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="技术面评分"
              value={data.technical_score?.toFixed(2) || '-'}
              suffix="分"
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="基本面评分"
              value={data.fundamental_score?.toFixed(2) || '-'}
              suffix="分"
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="资金面评分"
              value={data.money_flow_score?.toFixed(2) || '-'}
              suffix="分"
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="综合评分"
              value={data.overall_score?.toFixed(2) || '-'}
              suffix="分"
              valueStyle={{ color: '#3f8600' }}
            />
          </Card>
        </Col>
      </Row>

      <Card title="分析结果">
        <Descriptions column={1}>
          <Descriptions.Item label="股票代码">{data.code}</Descriptions.Item>
          <Descriptions.Item label="股票名称">{data.name}</Descriptions.Item>
          <Descriptions.Item label="分析建议">{data.reason || '-'}</Descriptions.Item>
          <Descriptions.Item label="技术面评分">
            {data.technical_score?.toFixed(2) || '-'} 分
          </Descriptions.Item>
          <Descriptions.Item label="基本面评分">
            {data.fundamental_score?.toFixed(2) || '-'} 分
          </Descriptions.Item>
          <Descriptions.Item label="资金面评分">
            {data.money_flow_score?.toFixed(2) || '-'} 分
          </Descriptions.Item>
          <Descriptions.Item label="综合评分">
            {data.overall_score?.toFixed(2) || '-'} 分
          </Descriptions.Item>
        </Descriptions>
      </Card>

      <Card
        title="免责声明"
        style={{ marginTop: 16 }}
        type="inner"
      >
        <p>
          本分析工具仅供学习和研究使用，不作为投资建议。使用本工具进行投资所产生的任何损失或收益，与本工具开发者无关。投资有风险，请根据自身情况谨慎决策。
        </p>
      </Card>
    </div>
  );
}

export default Analysis;
