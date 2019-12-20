/ *检测连通域，并删除不符合条件的连通域 * /
    void
    findConnectedDomain(Mat &srcImg, vector<vector<Point>> &connectedDomains, int area, int WHRatio)
{
    Mat_<uchar> tempImg = (Mat_<uchar> &)
        srcImg;

    for (int i = 0; i < tempImg.rows; ++i)
    {
        uchar *row = tempImg.ptr(i); // // 调取存储图像内存的第i行的指针
        for (int j = 0; j < tempImg.cols; ++j)
        {
            if (row[j] == 255)
            {
                stack<Point> connectedPoints;
                vector<Point> domain;
                connectedPoints.push(Point(j, i));
                while (!connectedPoints.empty())
                {
                    Point currentPoint = connectedPoints.top();
                    domain.push_back(currentPoint);

                    int colNum = currentPoint.x;
                    int rowNum = currentPoint.y;

                    tempImg.ptr(rowNum)[colNum] = 0;
                    connectedPoints.pop();

                    if (rowNum - 1 >= 0 & &colNum - 1 >= 0 & &tempImg.ptr(rowNum - 1)[colNum - 1] == 255)
                    {
                        tempImg.ptr(rowNum - 1)[colNum - 1] = 0;
                        connectedPoints.push(Point(colNum - 1, rowNum - 1));
                    }
                    if (rowNum - 1 >= 0 & &tempImg.ptr(rowNum - 1)[colNum] == 255)
                    {
                        tempImg.ptr(rowNum - 1)[colNum] = 0;
                        connectedPoints.push(Point(colNum, rowNum - 1));
                    }
                    if (rowNum - 1 >= 0 & &colNum + 1 < tempImg.cols & &tempImg.ptr(rowNum - 1)[colNum + 1] == 255)
                    {
                        tempImg.ptr(rowNum - 1)[colNum + 1] = 0;
                        connectedPoints.push(Point(colNum + 1, rowNum - 1));
                    }
                    if (colNum - 1 >= 0 & &tempImg.ptr(rowNum)[colNum - 1] == 255)
                    {
                        tempImg.ptr(rowNum)[colNum - 1] = 0;
                        connectedPoints.push(Point(colNum - 1, rowNum));
                    }
                    if (colNum + 1 < tempImg.cols & &tempImg.ptr(rowNum)[colNum + 1] == 255)
                    {
                        tempImg.ptr(rowNum)[colNum + 1] = 0;
                        connectedPoints.push(Point(colNum + 1, rowNum));
                    }
                    if (rowNum + 1 < tempImg.rows & &colNum - 1 > 0 & &tempImg.ptr(rowNum + 1)[colNum - 1] == 255)
                    {
                        tempImg.ptr(rowNum + 1)[colNum - 1] = 0;
                        connectedPoints.push(Point(colNum - 1, rowNum + 1));
                    }
                    if (rowNum + 1 < tempImg.rows & &tempImg.ptr(rowNum + 1)[colNum] == 255)
                    {
                        tempImg.ptr(rowNum + 1)[colNum] = 0;
                        connectedPoints.push(Point(colNum, rowNum + 1));
                    }
                    if (rowNum + 1 < tempImg.rows & &colNum + 1 < tempImg.cols & &tempImg.ptr(rowNum + 1)[colNum + 1] == 255)
                    {
                        tempImg.ptr(rowNum + 1)[colNum + 1] = 0;
                        connectedPoints.push(Point(colNum + 1, rowNum + 1));
                    }
                }
                if (domain.size() > area)
                {
                    RotatedRect rect = minAreaRect(domain);
                    float width = rect.size.width;
                    float height = rect.size.height;
                    if (width < height)
                    {
                        float temp = width;
                        width = height;
                        height = temp;
                    }
                    if (width > height * WHRatio & &width > 50)
                    {
                        for (auto cit = domain.begin(); cit != domain.end(); ++cit)
                        {
                            tempImg.ptr(cit->y)[cit->x] = 250;
                        }
                        connectedDomains.push_back(domain);
                    }
                }
            }
        }
    }

    binaryzation(srcImg);
}